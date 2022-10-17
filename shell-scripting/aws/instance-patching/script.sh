# !/bin/bash
# Before executing the script, it is assumed that the EC2 instances are correctly labeled
# Also the baseline is created and configured with its respective path groups
# Version 1.2
# Creation date: 12/10/2022

# Parameter $1 = tag=Key (Patch Group)
# Parameter $2 = tag=Value (Dev)
# Parameter $3 = region (us-east-1)

# Global variables
_key=$1
_value=$2
_region=$3
_key_ami_delete=$4
_value_ami_delete=$5
_amiBackups=()
_commandId=""

# Checking the AMI status
function validate_state_ami(){
    
    # Getting the AMI id from _amiBackups array
    for ami in `echo $_amiBackups | tr "," "\n" | sed '/^ *$/d'`
    do
        # Getting the AMI status
        local amiAvailable=$(aws ec2 describe-images \
            --image-ids ${ami} \
            --output json |  jq -r '.Images[].State')

        # If the status is different from available return false
        if [[ $amiAvailable != "available" ]]
        then
            local result="false"
            echo $result
            break
        fi
    done

    # If all status AMIs are available, return true
    local result="true"
    echo $result
}

# Checking the instance patching status
function validate_instance_patching(){

    # Local variables
    local counter=1

    # Getting the instances that are being patched
    local instancePatching=$(aws ssm list-command-invocations \
        --command-id $_commandId \
        --details | jq -r '.CommandInvocations[].InstanceId')

    # Iterate the instances list
    for instance in $instancePatching
    do
        # Getting the four status
        local instanceState=$(aws ssm list-command-invocations \
            --command-id $_commandId \
            --instance-id $instance \
            --details | jq -r '.CommandInvocations[].Status')

         # Checking if the instance state is different from Success
        if [[ $instanceState != "Success" ]]
        then
            local result="false"
            echo $result
            break
        fi
    done

    local result="true"
    echo $result
}

# List all candidate instances to be patched
function candidate_instances(){

    # Local variables and texts
    local counter=1
    echo -e "Generando backup de instancias EC2 que se van a parchar...\n"

    # Describes an instance that has a specific tag
    local instanceIds=$(aws ec2 describe-instances \
        --region ${_region} \
        --filters "Name=tag:${_key},Values=${_value}" \
        --output json | jq -r '.Reservations[].Instances[].InstanceId')

    # Creation the instance backup (AMI)
    for instance in $instanceIds
    do
        # Adds the AMI id to the _amiBackups array
        _amiBackups+=$(aws ec2 create-image --instance-id $instance \
            --name "$instance-$(date +'%d/%m/%Y_%H_%M_%S-UTC')" \
            --description "AMI creada pre parchado $instance" \
            --no-reboot \
            --region ${_region} \
            --tag-specifications \
            "ResourceType=image,Tags=[{Key='$_key_ami_delete',Value='$_value_ami_delete'},{Key=Name,Value='$instance'}]" \
            "ResourceType=snapshot,Tags=[{Key='$_key_ami_delete',Value='$_value_ami_delete'},{Key=Name,Value='$instance'}]" \
            --output text),
    done    

    # Checks the AMI status 3 times every 3 minutes,
    # if it passes all three times, it breaks the validation
    while [ $counter -lt 4 ]
    do  
        # Validates the value returned by the validate_state_ami function
        # if the value is true, the AMI are in available state
        sleep 180
        local state=$(validate_state_ami)

        # Validates the returned value
        if [[ $state == "true" ]]
        then
            echo "AMIs disponibles"
            break
        fi

        # Waiting for the next check
        echo "Las AMIS no está disponibles por el momento..."
        echo -e "Esperando 3 minutos para volver a comprobar el estado de las AMI $counter/3\n"
        let counter++
    done
}

# Function to patch instances
function patching(){

    # Local variables
    local counter=1

    # Getting the command id
    _commandId=$(aws ssm send-command \
        --region ${_region} \
        --document-name "AWS-RunPatchBaseline" \
        --targets Key="tag:${_key}",Values="$_value" \
        --parameters "Operation=Install" \
        --timeout-seconds 600 \
        --output json | jq -r '.Command.CommandId')

    # Checking three times every five minutes if the instances are ok
    while [ $counter -lt 4 ]
    do
        # Validates the value returned by the validate_instance_patching function
        # if the value is true, the instances were patched
        sleep 300
        local state=$(validate_instance_patching)

        # Validates the returned value
        if [[ $state == "true" ]]
        then 
            echo "Todas las instancias se parcharon exitosamente"
            break
        fi

        # Waiting for the next check
        echo "No se han parchado todas las instancias"
        echo -e "Esperando 5 minutos para volver a comprobar el estado $counter/3\n"
        let counter++
    done
}

candidate_instances