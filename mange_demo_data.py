import os
import click
from amp_client import AMP
from amp_client import utilities


def demo_data_message(method=None):
    messages = {
        "delete": "Disabling Demo Data",
        "put": "Refreshing Demo Data",
        None: "Enabling Demo Data",
    }

    print(messages[method])


def manage_demo_date(session, authenticity_token, method=None):
    url = "https://console.amp.cisco.com/demo_data"

    data = {"authenticity_token": authenticity_token}

    if method:  # can be put or delete
        data["_method"] = method

    demo_data_message(method)
    response = session.post(url, data=data)
    return response


@click.command()
@click.option("-u", "--user", prompt=True, help="Cisco Security account email address")
@click.option(
    "-p",
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Cisco Security account password",
)
@click.option(
    "-r",
    "--region",
    prompt=True,
    type=click.Choice(["APJC", "EU", "NAM"], case_sensitive=False),
    help="AMP for Endpoints region to authenticate to",
)
@click.option(
    "-a",
    "--action",
    prompt=True,
    type=click.Choice(["enable", "disable", "refresh"], case_sensitive=False),
    help="The action to take with demo data",
)
def main(**kwags):
    """ Authenticate to AMP for Endpoints Console using a Cisco Security account
    Download connector for chosen OS, group, and settings and save to disk
    """
    user = kwags.get("user")
    password = kwags.get("password")
    region = kwags.get("region")
    action = kwags.get("action")

    # Create AMP for Endpoints client, check for Two Factor Auth secret as an environment variable
    amp_client = AMP(user, password, region, os.getenv("AMP_TOTP_SECRET"))

    # Authenticate to AMP for Endpoints
    amp_client.authenticate()
    print("Authentication Successful")

    session = amp_client.session
    authenticity_token = amp_client.authenticity_token

    action_mapping = {"enable": None, "disable": "delete", "refresh": "put"}

    response = manage_demo_date(session, authenticity_token, action_mapping[action])

    print(response)
    # print(response.text)


if __name__ == "__main__":
    main()
