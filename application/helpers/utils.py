import pandas as pd
from azure.core.exceptions import ResourceExistsError
from azure.data.tables import TableClient, UpdateMode
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from multielo import MultiElo


SUBSCRIPTION_ID = "2293b5f9-5144-48c3-9e63-605f45ecbc1e"
GROUP_NAME = "platform-tetris-dev"
STORAGE_ACCOUNT_NAME = "stractdev"


def get_table_client():
    credential = DefaultAzureCredential()
    storage_client = StorageManagementClient(credential, SUBSCRIPTION_ID)
    storage_keys = storage_client.storage_accounts.list_keys(GROUP_NAME, STORAGE_ACCOUNT_NAME)
    storage_keys = {v.key_name: v.value for v in storage_keys.keys}
    key = storage_keys["key1"]
    table_client = TableClient.from_connection_string(
        conn_str=f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={key};EndpointSuffix=core.windows.net", table_name="users"
    )
    return table_client

def get_leaderboard_data():
    table_client = get_table_client()
    my_filter = "PartitionKey eq 'Users'"
    entities = table_client.query_entities(query_filter=my_filter, select=["User", "MMR"])

    pd.set_option("display.width", 1000)
    pd.set_option("colheader_justify", "center")

    leaderboard_df = pd.DataFrame(entities)
    sort = leaderboard_df.sort_values(by=["MMR"], ascending=False)
    tables = sort.to_html(classes="leaderboard", header="true", index=False)
    return tables

def get_or_create_users(table_client, usernames):
    users=[]
    for username in usernames:
        try:
            entity={"PartitionKey": "Users", "RowKey": username.lower(),"User": username, "MMR": "1000"}
            table_client.create_entity(entity)
            users.append(entity)
        except ResourceExistsError:
            print(f"""User: {username} already exists!""")
            entity = table_client.get_entity(partition_key="Users", row_key=username.lower())
            users.append(entity)
    return users

def update_users(table_client, users):
    for user in users:
        table_client.update_entity(
            mode=UpdateMode.MERGE, entity=user
        )

def calc_mmr(usernames):
    table_client = get_table_client()
    users = get_or_create_users(table_client, usernames)
    elo = MultiElo()
    new_ratings = elo.get_new_ratings([int(user["MMR"]) for user in users])
    for i, new_rating in enumerate(new_ratings):
        users[i]["MMR"] = str(round(new_rating))
    update_users(table_client, users)
    return users