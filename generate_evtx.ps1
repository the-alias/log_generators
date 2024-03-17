# Define log source and name based on realistic scenarios
$logSource = "Microsoft-Windows-Security-Auditing"
$logName = "Security"

# Check and create log source if it doesn't exist
if (-not [System.Diagnostics.EventLog]::SourceExists($logSource)) {
    [System.Diagnostics.EventLog]::CreateEventSource($logSource, $logName)
}

function Get-DetailedEventMessage {
    param (
        [Parameter(Mandatory = $true)][int]$EventID
    )

    $domainPart = "1000-1001-1002" # Simulated domain part of SID
    $userRID = Get-Random -Minimum 1000 -Maximum 1100 # Random RID for user

    switch ($EventID) {
        4624 { # User Login Success
            $userSID = "S-1-5-21-" + $domainPart + "-" + $userRID
            return "Successful login for SID $userSID"
        }
        4625 { # User Login Failure
            $userSID = "S-1-5-21-" + $domainPart + "-" + $userRID
            return "Failed login attempt for SID $userSID"
        }
        4648 { # Explicit Credential Logon
            $userSID = "S-1-5-21-" + $domainPart + "-" + $userRID
            return "Explicit credentials used to login as SID $userSID"
        }
        4662 { # Object Operation
            $objectName = "File", "RegistryKey", "Directory" | Get-Random
            return "$objectName object was accessed"
        }
        4670 { # Permissions on an object were changed
            $objectName = "File", "RegistryKey", "Directory" | Get-Random
            return "Permissions on $objectName object were changed"
        }
        4720 { # A user account was created
            $userSID = "S-1-5-21-" + $domainPart + "-" + $userRID
            return "A user account was created with SID $userSID"
        }
        4722 { # A user account was enabled
            $userSID = "S-1-5-21-" + $domainPart + "-" + $userRID
            return "A user account was enabled with SID $userSID"
        }
        4725 { # A user account was disabled
            $userSID = "S-1-5-21-" + $domainPart + "-" + $userRID
            return "A user account was disabled with SID $userSID"
        }
        4732 { # A member was added to a security-enabled local group
            $groupName = "Administrators", "Users", "Guests" | Get-Random
            return "A member was added to the $groupName group"
        }
        4738 { # A user account was changed
            $userSID = "S-1-5-21-" + $domainPart + "-" + $userRID
            return "A user account with SID $userSID was changed"
        }
        4740 { # A user account was locked out
            $userSID = "S-1-5-21-" + $domainPart + "-" + $userRID
            return "A user account with SID $userSID was locked out"
        }
        4756 { # A member was added to a security-enabled universal group
            $groupName = "Remote Desktop Users", "Network Configuration Operators" | Get-Random
            return "A member was added to the $groupName group"
        }
        4776 { # The computer attempted to validate the credentials for an account
            $userSID = "S-1-5-21-" + $domainPart + "-" + $userRID
            return "Credentials for an account with SID $userSID were validated"
        }
        4781 { # The name of an account was changed
            $oldName = "User" + (Get-Random -Minimum 1 -Maximum 500)
            $newName = "User" + (Get-Random -Minimum 501 -Maximum 1000)
            return "The account name was changed from $oldName to $newName"
        }
        4798 { # A user's local group membership was enumerated
            $userSID = "S-1-5-21-" + $domainPart + "-" + $userRID
            return "Local group membership for SID $userSID was enumerated"
        }
        4799 { # A security-enabled local group membership was enumerated
            $userSID = "S-1-5-21-" + $domainPart + "-" + $userRID
            return "Security-enabled local group membership for SID $userSID was enumerated"
        }
        1102 { # The audit log was cleared
            return "The audit log was cleared"
        }
        4616 { # The system time was changed
            return "The system time was changed"
        }
        4698 { # A scheduled task was created
            return "A scheduled task was created"
        }
        4699 { # A scheduled task was deleted
            return "A scheduled task was deleted"
        }
        4702 { # A scheduled task was updated
            return "A scheduled task was updated"
        }
        Default {
            return "An event occurred with ID $EventID"
        }
    }
}


function Write-WeightedLogEntry {
    param (
        [Parameter(Mandatory = $true)][System.Collections.Hashtable]$eventWeights,
        [Parameter(Mandatory = $true)][string]$logSource
    )
    
    $totalWeight = 0
    foreach ($weight in $eventWeights.Values.Weight) {
        $totalWeight += $weight
    }

    $randomWeight = Get-Random -Minimum 1 -Maximum $totalWeight
    $cumulativeWeight = 0
    foreach ($event in $eventWeights.GetEnumerator()) {
        $cumulativeWeight += $event.Value.Weight
        if ($cumulativeWeight -ge $randomWeight) {
            $eventId = $event.Key
            $message = Get-DetailedEventMessage -EventID $eventId
            Write-EventLog -LogName $logName -Source $logSource -EntryType Information -EventID $eventId -Message $message
            break
        }
    }
}

# Placeholder for event weights hashtable
$eventWeights = @{
    4624 = @{ Weight = 30; Description = "User Login Success" }
    4625 = @{ Weight = 20; Description = "User Login Failure" }
    4648 = @{ Weight = 15; Description = "Explicit Credential Logon" }
    4662 = @{ Weight = 10; Description = "Object Operation" }
    4670 = @{ Weight = 5; Description = "Permissions on an object were changed" }
    4720 = @{ Weight = 8; Description = "A user account was created" }
    4722 = @{ Weight = 8; Description = "A user account was enabled" }
    4725 = @{ Weight = 4; Description = "A user account was disabled" }
    4732 = @{ Weight = 7; Description = "A member was added to a security-enabled local group" }
    4738 = @{ Weight = 7; Description = "A user account was changed" }
    4740 = @{ Weight = 6; Description = "A user account was locked out" }
    4756 = @{ Weight = 5; Description = "A member was added to a security-enabled universal group" }
    4776 = @{ Weight = 10; Description = "The computer attempted to validate the credentials for an account" }
    4781 = @{ Weight = 4; Description = "The name of an account was changed" }
    4798 = @{ Weight = 3; Description = "A user's local group membership was enumerated" }
    4799 = @{ Weight = 3; Description = "A security-enabled local group membership was enumerated" }
    1102 = @{ Weight = 2; Description = "The audit log was cleared" }
    4616 = @{ Weight = 1; Description = "The system time was changed" }
    4698 = @{ Weight = 2; Description = "A scheduled task was created" }
    4699 = @{ Weight = 2; Description = "A scheduled task was deleted" }
    4702 = @{ Weight = 2; Description = "A scheduled task was updated" }
}

# Generate logs
for ($i = 0; $i -lt 10000; $i++) {
    Write-WeightedLogEntry -eventWeights $eventWeights -logSource $logSource
}

# Define the path for the .evtx file
$evtxPath = Join-Path -Path $env:USERPROFILE -ChildPath "Desktop\CustomAppLog.evtx"

# Export the log using wevtutil
wevtutil epl $logName $evtxPath /ow

Write-Output "Log exported to $evtxPath"
