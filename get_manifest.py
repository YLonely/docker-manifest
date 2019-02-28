import json
import pymysql
import subprocess

file_path = "./new_name2.txt"
docker_command = 'docker manifest inspect -v {0}'
insert_image_info = "insert ignore into image_info(image_id,namespace,repo_name,tag,arch,os,layers,created_at,updated_at,category,size) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')"
insert_layer_info = "insert ignore into layer_info(layer_id,image_id,size) values ('{0}','{1}','{2}')"
db = pymysql.connect("localhost", "root", "****", "manifest")
cursor = db.cursor()


def get_attr(manifest):
    arch = manifest['Descriptor']['platform']['architecture']
    os = manifest['Descriptor']['platform']['os']
    image_id = manifest['SchemaV2Manifest']['config']['digest']
    size = manifest['SchemaV2Manifest']['config']['size']
    layers = manifest['SchemaV2Manifest']['layers']
    return arch, os, image_id, size, layers


def db_insert(image_id, namespace, repo_name, tag, arch, os, layers, created_at, updated_at, category, size):
    layers_id = []
    try:
        for layer in layers:
            cursor.execute(insert_layer_info.format(
                layer['digest'], image_id, layer['size']))
            layers_id.append(layer['digest'])
        command = insert_image_info.format(
            image_id, namespace, repo_name, tag, arch, os, ','.join(layers_id), created_at, updated_at, category, size)
        cursor.execute(command)
        db.commit()
    except:
        db.rollback()
        print("Error:"+command)
        exit()


with open(file_path, 'r') as f:
    lines = f.readlines()
sum = len(lines)
i = 1
for line in lines:
    parts = line.split(',')
    namespace_repo_tag = parts[0]
    if "ERROR" in namespace_repo_tag:
        continue
    created_at = parts[1][:19]
    updated_at = parts[2][:19]
    category = parts[3]
    if ':' in namespace_repo_tag:
        namespace_repo, tag = namespace_repo_tag.split(':')
    else:
        namespace_repo, tag = namespace_repo_tag, 'latest'
    if '/' in namespace_repo:
        t = namespace_repo.split('/')
        namespace = t[0]
        repo = '/'.join(t[1:])
    else:
        namespace = 'libiary'
        repo = namespace_repo
    manifest_info = subprocess.getoutput(
        docker_command.format(namespace_repo_tag))
    if '[' not in manifest_info or '{' not in manifest_info:
        print("ERROR:"+namespace_repo_tag)
        continue
    manifest_json = json.loads(manifest_info)
    if type(manifest_json) == list:
        for manifest in manifest_json:
            arch, os, image_id, size, layers = get_attr(manifest)
            db_insert(image_id, namespace, repo, tag, arch,
                      os, layers, created_at, updated_at, category, size)
    else:
        arch, os, image_id, size, layers = get_attr(manifest_json)
        db_insert(image_id, namespace, repo, tag, arch,
                  os, layers, created_at, updated_at, category, size)
db.close()
