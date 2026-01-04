# GitHub 仓库连接脚本
# 使用方法：在PowerShell中运行：.\setup_github.ps1

Write-Host "=== GitHub 仓库连接助手 ===" -ForegroundColor Cyan
Write-Host ""

# 检查是否已配置远程仓库
$remote = git remote get-url origin 2>$null
if ($remote) {
    Write-Host "当前已配置的远程仓库: $remote" -ForegroundColor Yellow
    $change = Read-Host "是否要更改远程仓库地址？(y/n)"
    if ($change -eq "y") {
        git remote remove origin
    } else {
        Write-Host "保持现有配置。" -ForegroundColor Green
        exit
    }
}

Write-Host ""
Write-Host "请选择连接方式：" -ForegroundColor Cyan
Write-Host "1. HTTPS (推荐，简单易用)"
Write-Host "2. SSH (需要配置SSH密钥)"
Write-Host ""
$choice = Read-Host "请输入选项 (1 或 2)"

Write-Host ""
$username = Read-Host "请输入你的 GitHub 用户名"
$repoName = Read-Host "请输入仓库名称"

if ($choice -eq "1") {
    $remoteUrl = "https://github.com/$username/$repoName.git"
} else {
    $remoteUrl = "git@github.com:$username/$repoName.git"
}

Write-Host ""
Write-Host "正在添加远程仓库: $remoteUrl" -ForegroundColor Yellow
git remote add origin $remoteUrl

Write-Host ""
Write-Host "正在重命名分支为 main..." -ForegroundColor Yellow
git branch -M main

Write-Host ""
Write-Host "=== 配置完成！===" -ForegroundColor Green
Write-Host ""
Write-Host "下一步操作：" -ForegroundColor Cyan
Write-Host "1. 在 GitHub 上创建仓库（如果还没有创建）"
Write-Host "2. 运行以下命令推送代码：" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "3. 配置 GitHub Secrets：" -ForegroundColor Yellow
Write-Host "   - 进入仓库 Settings → Secrets and variables → Actions"
Write-Host "   - 添加 PUSH_KEY secret（你的 PushPlus token）"
Write-Host ""
Write-Host "详细说明请查看 GITHUB_SETUP.md 文件" -ForegroundColor Cyan

