$headers = @{
    'Authorization' = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlNDhlNDlkMDQ1ZDM0MGFiYTYxNmY4NDNmYTVhZjljYiIsImlhdCI6MTc2NzMwNzU2NiwiZXhwIjoyMDgyNjY3NTY2fQ.icoUlwaLQdx5atxNGQWCYJ9oAmyLwiMTZcHfCqPwUh4'
    'Content-Type' = 'application/json'
}

$action = $args[0]

switch ($action) {
    "list-repos" {
        $result = Invoke-RestMethod -Uri 'http://192.168.1.221:8123/api/hassio/store/repositories' -Headers $headers -Method Get
        $result | ConvertTo-Json -Depth 10
    }
    "list-addons" {
        $result = Invoke-RestMethod -Uri 'http://192.168.1.221:8123/api/hassio/addons' -Headers $headers -Method Get
        $result | ConvertTo-Json -Depth 10
    }
    "uninstall-stash" {
        $result = Invoke-RestMethod -Uri 'http://192.168.1.221:8123/api/hassio/addons/caf8d8ae_stash/uninstall' -Headers $headers -Method Post
        $result | ConvertTo-Json -Depth 5
    }
    "remove-repo" {
        $body = @{
            repository = 'https://github.com/zer0sis/hass-addons'
        } | ConvertTo-Json
        $result = Invoke-RestMethod -Uri 'http://192.168.1.221:8123/api/hassio/store/repositories' -Headers $headers -Method Delete -Body $body
        $result | ConvertTo-Json -Depth 5
    }
    "add-repo" {
        $body = @{
            repository = 'https://github.com/zer0sis/hass-addons'
        } | ConvertTo-Json
        $result = Invoke-RestMethod -Uri 'http://192.168.1.221:8123/api/hassio/store/repositories' -Headers $headers -Method Post -Body $body
        $result | ConvertTo-Json -Depth 5
    }
    "install-stash" {
        $result = Invoke-RestMethod -Uri 'http://192.168.1.221:8123/api/hassio/addons/caf8d8ae_stash/install' -Headers $headers -Method Post
        $result | ConvertTo-Json -Depth 5
    }
    "start-stash" {
        $result = Invoke-RestMethod -Uri 'http://192.168.1.221:8123/api/hassio/addons/caf8d8ae_stash/start' -Headers $headers -Method Post
        $result | ConvertTo-Json -Depth 5
    }
    "stash-info" {
        $result = Invoke-RestMethod -Uri 'http://192.168.1.221:8123/api/hassio/addons/caf8d8ae_stash/info' -Headers $headers -Method Get
        $result | ConvertTo-Json -Depth 5
    }
    "stash-logs" {
        $result = Invoke-RestMethod -Uri 'http://192.168.1.221:8123/api/hassio/addons/caf8d8ae_stash/logs' -Headers $headers -Method Get
        $result
    }
    "refresh" {
        $result = Invoke-RestMethod -Uri 'http://192.168.1.221:8123/api/hassio/store/reload' -Headers $headers -Method Post
        $result | ConvertTo-Json -Depth 5
    }
    default {
        Write-Host "Usage: ha_api.ps1 <action>"
        Write-Host "Actions: list-repos, list-addons, uninstall-stash, remove-repo, add-repo, install-stash, start-stash, stash-info, stash-logs, refresh"
    }
}
