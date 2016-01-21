import os


rundeck_host = "10.74.113.101"
project_path = "/var/rundeck/projects/dms-sa"

#rundeck_host = "10.74.125.196"
#project_path = "/Users/yanhao/Desktop/dms/rundeck/dms-sa"

token = "hAdmwI1dv0cnaVHyQcO6Wr3tvFrp8LUt"
res_path = os.path.join(project_path,"resources")
job_path = os.path.join(project_path,"job_templates")


url_base =  "http://%s:4440" % (rundeck_host)
url_list_resources = url_base + "/api/14/project/dms-sa/resources"
url_create_job = url_base + "/api/15/project/dms-sa/jobs/import?uuidOption=remove"
url_run_job = url_base + "/api/1/job/%s/run"
url_query_job = url_base + "/api/14/project/dms-sa/jobs?jobExactFilter=%s"
url_delete_job = url_base + "/api/1/job/%s"

ansible_execute_path = "/usr/local/bin"
ansible_playbook_file_path = os.path.join(project_path,"scripts/dms_sa/lib/rdeck_ansible/ansible")

