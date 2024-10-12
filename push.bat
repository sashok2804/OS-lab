@echo off
git status
:: Запрашиваем имя коммита
set /p commitName="Commit name (!!!): "

if "%commitName%"=="" (
    echo Ошибка: Error! Pls input commit name
    exit /b 1
)

set /p commitComment="Commit coment (ne obyaz): "

git add .

if "%commitComment%"=="" (
    git commit -m "%commitName%"
) else (
    git commit -m "%commitName%" -m "%commitComment%"
)

git push

echo Коммит и пуш завершены.
pause
