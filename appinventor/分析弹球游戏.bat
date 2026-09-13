@echo off
chcp 65001 >nul
cd /d "d:\pycharm\Qwen"
echo 正在分析弹球游戏.aia...
echo.
python extract_ref.py > ref_extracted.txt 2>&1
echo 分析完成！结果已保存到 ref_extracted.txt
echo.
type ref_extracted.txt
pause
