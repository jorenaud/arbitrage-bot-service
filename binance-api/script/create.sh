res=$(sudo kubectl create ns $1)
res=$(sudo kubectl create -f yaml/ -n $1)
echo "{"
echo "\"ports\": \"""$(sudo kubectl get svc -n $1 | grep moodle-project-moodle | awk '{print $5}')""\","
echo "\"password\": \"""$(sudo kubectl get secret -n $1 moodle-project-moodle -o jsonpath='{.data.moodle-password}' | base64 --decode)""\""
echo "}"

