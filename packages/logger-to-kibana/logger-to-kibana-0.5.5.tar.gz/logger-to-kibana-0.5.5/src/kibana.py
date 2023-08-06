"""
This function handles the generation of the kibana visualization
"""
from src.configuration import config

import requests
from src.utils import visualization
from src.utils import dashboard
from src.aws_credentials import aws_auth
from itertools import groupby


def generate_and_send_visualizations(folder_name: str, items: []):
    grouped_items = group_items(items)
    if grouped_items:
        generated_ids = []
        for group in grouped_items:
            title = get_title_from_group(folder_name, group[0])
            vis = generate_folder_visualization(title, group)
            generated_ids.append(send_visualization(title, vis))
        generated_dashboard = dashboard.generate_dashboard(folder_name,
                                                           generated_ids)
        send_dashboard(folder_name, generated_dashboard)


def get_title_from_group(folder_name: str, group: dict) -> str:
    return (f"{folder_name} {group['subfolder']} "
            f"{group['filename']} {group['function']}")


def generate_folder_visualizations(folder_name: str, items: []) -> []:
    result = []
    grouped_items = group_items(items)
    if grouped_items:
        for group in grouped_items:
            title = get_title_from_group(folder_name, group[0])
            result.append(generate_folder_visualization(title, group))
    return result


def group_items(items: []) -> []:
    groups = []
    sorted_reader = sorted(items, key=lambda d:
                           (d['subfolder'], d['filename'], d['function']))
    for k, g in groupby(sorted_reader, key=lambda d:
                        (d['subfolder'], d['filename'], d['function'])):
        groups.append(list(g))
    return groups


def generate_folder_visualization(folder_name: str, items: []) -> dict:
    return visualization.generate_visualization(folder_name, items)


def send_visualization(folder_name: str, attributes: dict) -> str:
    headers = {"kbn-xsrf": "true"}
    data = {"attributes": attributes}
    generated_id = f"generated-{folder_name}"
    url = (
        f"""{config.kibana.BaseUrl}/api/saved_objects/visualization/"""
        f"""{generated_id}?overwrite=true"""
    )
    auth = aws_auth() if (config.kibana.AuthType == "aws") else None

    response = requests.post(
        url,
        json=data,
        headers=headers,
        auth=auth,
    )

    print(response.text)
    return str(generated_id)


def send_dashboard(folder_name: str, attributes: dict):
    headers = {"kbn-xsrf": "true"}
    data = {"attributes": attributes}
    url = (
        f"""{config.kibana.BaseUrl}/api/saved_objects/dashboard/"""
        f"""generated-{folder_name}?overwrite=true"""
    )
    auth = aws_auth() if (config.kibana.AuthType == "aws") else None

    response = requests.post(
        url,
        json=data,
        headers=headers,
        auth=auth,
    )

    print(response.text)
