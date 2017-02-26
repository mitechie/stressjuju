"""
This example:

1. Connects to the current model
2. Deploy a charm and waits until it reports itself active
3. Destroys the unit and application

"""
import asyncio
import click
import logging

from juju import loop
from juju.client.connection import JujuData
from juju.controller import Controller
from juju.errors import JujuAPIError
from juju.model import Model


log = logging.getLogger(__name__)


@click.command()
@click.option('--controller', '-c', help="Controller to stress test.")
@click.option(
    '--num-runs', '-n', default=1, type=int,
    help="How many models to create/destroy")
@click.option('--parallel', '-p', default=1, type=int,
              help="How many at a time to perform these.")
@click.argument('deploy', nargs=1, type=str)
def run(deploy, controller, num_runs, parallel):

    loop = asyncio.get_event_loop()
    loop.set_debug(False)

    # Figure out how many runs we're going to need to do.
    run = 0
    while run < num_runs:
        running = []
        while run < num_runs and len(running) < parallel:
            log.info("Running model number {}".format(run))
            running.append(
                loop.create_task(stress(loop, controller, run, deploy))
            )
            run = run + 1
        loop.run_until_complete(asyncio.gather(
            *running
        ))
    loop.close()


async def stress(loop, controller, model_id, deploy):
    model_name = "{}-{}".format('stress', model_id)
    data = JujuData()
    controllers = data.controllers()
    if controller not in controllers:
        log.error('Controller {} not found'.format(controller))
        return
    target = controllers[controller]
    cont = Controller()

    # Blocking call which returns when the display_date() coroutine is done
    await cont.connect_controller(controller)
    stress = await cont.add_model(model_name,
                                  credential_name='guimaas-rharding')
    # add_model will auto connect to the model that's returned.
    log.debug('Deploying {}'.format(deploy))
    bundle_deploy = await stress.deploy(deploy)

    log.debug('Waiting for active')
    while not is_deployed(bundle_deploy):
        # wait a second and try again
        await asyncio.sleep(1)

    log.debug('Destroying the model: {}'.format(model_name))
    await cont.destroy_models(stress.info.uuid)
    await stress.disconnect()
    await cont.disconnect()


def is_deployed(applications):
    for application in applications:
        for unit in application.units:
            # have to use active or unknown. Active is for charms using the
            # newer status tools and unknown is for older charms that don't
            # report status.
            if unit.workload_status not in ('active', 'unknown'):
                return False
    return True


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    ws_logger = logging.getLogger('websockets.protocol')
    ws_logger.setLevel(logging.INFO)
    run()
