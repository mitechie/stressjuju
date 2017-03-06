Monitoring your controllers
===========================


These steps help walk you through setting up Prometheus watching of your
controllers and setting up Grafana to help visualize your production Juju
infrastructure.




![alt text](https://c1.staticflickr.com/1/737/33070753722_75ab25ed9f.jpg" Sample Dashboard")

Prometheus Setup
----------------

You need to bootstrap your controller and then add Prometheus to the
controller machine.

    juju bootstrap aws
    juju switch controller
    juju deploy cs:~prometheus-charmers/prometheus --to 0
    juju deploy cs:telegraf

    # This relation will tell telgraf to monitor the machine
    juju relate telegraf:juju-info prometheus:juju-info
    juju expose telegraf
    # This relation is to add the telegraf /metrics endpoint to prometheus for graphing.
    juju relate telegraf:prometheus-client prometheus:target

You can check the is coming in on telegraf if you first expose telegraf.

    juju expose telegraf
    http://$CONTROLLER_IP:9103/metrics

Next up, configure Prometheus with the Juju target data.

    # Note that you don't need to register with this 'bot' user
    juju add-user prometheus
    juju change-user-password prometheus
    juju grant prometheus read controller
    # I've not been able to get the ca-cert working yet so have disabled cert
    # checking for the moment. This is a bug to be addressed.
    # juju controller-config ca-cert > juju-ca.crt
    # juju scp juju-ca.crt prometheus — need to figure out how to get the crt to work

Once the Juju info is setup you need to then add that target to prometheus.
You can edit the file `controller-prom.yml` included with the correct IP
address and username/password for your controller.

    juju config prometheus scrape-jobs=@controller-prom.yaml


Setting up graphical dashboard
------------------------------

To get a dashboard setup you need to deploy Grafana that will visualize the
Prometheus data. Make sure to choose your own password for the Grafana
instance. You may optionally also deploy this onto the controller itself, but
note that you'll need to be able to expose it to get access so deploying it
into a container on the host isn't always going to work on all providers.


    juju deploy cs:~prometheus-charmers/grafana
    # This doesn't work for me but should so will look into it
    # juju run --service grafana "scripts/get_admin_password"
    juju config grafana admin_password=$PASSWORD


Now log into your Grafana url

- http://$ipaddr:3000
- username: admin
- password: $whatever_you_set_in_above_config


and setup the data source to your Prometheus instance.

- data type prometheus
- direct access
- http://$ipaddr:9090

And you can load the included default `controller-dashboard.json` to have a
preconfigured graph.


Roadmap
-----------

- automate this more with scripting using python-libjuju
- add mongodb data for the juju data store to the graphs

