param(
    [Parameter(Mandatory=$true)][int]$SolidWorksPid,
    [Parameter(Mandatory=$true)][string]$Repository,
    [Parameter(Mandatory=$true)][string]$Cache,
    [string]$SolidWorksDirectory='G:\App\sw2024\SOLIDWORKS'
)
$ErrorActionPreference='Stop'
$interop=Join-Path $SolidWorksDirectory 'SolidWorks.Interop.sldworks.dll'
Add-Type -Path $interop
Add-Type -Path @((Join-Path $PSScriptRoot 'SwRot.cs'),(Join-Path $PSScriptRoot 'ExportReview.cs')) -ReferencedAssemblies $interop
[ExportReview]::Run($SolidWorksPid,$Repository,$Cache)
