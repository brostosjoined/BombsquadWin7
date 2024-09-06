# BombSquad Windows 7 Patch

This project provides a patch to make the latest version of **BombSquad** `CLIENT/SERVER` **1.7.19 for server** work on Windows 7. The patch involves using a Python modification that enables compatibility with Windows 7. 

## Installation Guide

Donwload the latest exe [here](dist/bsw7_patch.exe). For client just place the exe in the folder containing the games executable and for the server place the exe inside the `dist` folder. Then run the exe.

<table>
  <tr>
    <th style="text-align:center;">CLIENT</th>
    <th style="text-align:center;">SERVER(1.7.19)</th>
  </tr>
  <tr>
    <td style="text-align:center;"><img src=client.png alt="CLIENT" width="500px"></td>
    <td style="text-align:center;"><img src=server.png alt="SERVER" width="500px"></td>
  </tr>
</table>

## Building 

### 1. Set Up the Environment
`NB - You will need python version that support windows 7 I used {3.8.6}`

1. **Create a Virtual Environment:**
   ```bash
   py -m venv myenv
   ```
2. **Activate the Virtual Environment:**
    ```bash
    .\myenv\Scripts\activate
    ```
3. **Upgrade pip:**
    ```bash
    python.exe -m pip install --upgrade pip
    ```
## 2. Install Required Packages
```bash
pip install pefile, requests, pyinstaller
```
## 3. Build the Executable
```bash
pyinstaller --onefile --icon=bsw7.ico bsw7_patch.py
```

## Acknowledgments

- **BombSquad**: Special thanks to [efroemling](https://github.com/efroemling/ballistica) for developing BombSquad and making it available. You can find the ballistica (Bombsquad game engine) project [here](https://github.com/efroemling/ballistica).
- **Python Patch for Windows 7**: Thanks to [adang1345](https://github.com/adang1345) for their work on making Python compatible with Windows 7. You can find their project [here](https://github.com/adang1345/PythonWin7).
- **DLL Support**: Thanks to [kobilutil](https://github.com/kobilutil/api-ms-win-core-path-HACK) for originally creating the `api-ms-win-core-path-HACK` project, which was later forked and enhanced by [nalexandru](https://github.com/nalexandru/api-ms-win-core-path-HACK).


## License

This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for details.

