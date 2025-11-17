# refresh_dashboard.ps1
$pbixPath = "C:\Users\admin\OneDrive\Documents\fake-store-pipeline\fake-store-dashboard.pbix"
Start-Process -FilePath "C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe" -ArgumentList "`"$pbixPath`""
Start-Sleep -Seconds 30
Stop-Process -Name "PBIDesktop"
