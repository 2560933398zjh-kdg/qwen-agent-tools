@echo off
chcp 65001 >nul
cd /d "d:\pycharm\Qwen"

echo ============================================
echo 第1步：提取弹球游戏.aia的内容
echo ============================================
python extract_ref.py > ref_extracted.txt 2>&1
echo 完成！
echo.

echo ============================================
echo 第2步：分析两个aia文件的差异  
echo ============================================
python full_analysis.py > full_analysis_result.txt 2>&1
echo 完成！
echo.

echo ============================================
echo 结果文件：
echo   ref_extracted.txt - 弹球游戏的完整内容
echo   full_analysis_result.txt - 详细对比分析
echo ============================================
echo.
echo 请把 ref_extracted.txt 的内容发给我！
pause
