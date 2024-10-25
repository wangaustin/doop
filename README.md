# doop
A Python script to find files with the same name and type, grouped by name, excluding hidden files and specified directories.

### How to Use
1. Download `doop.py`
2. Move the downloaded `doop.py` to the directory you wish to perform the duplicate check
3. Run `doop.py` from that directory

### User Selection
1. Do you want to exclude any directories? (yes/no)
    - Enter the full paths of directories to exclude (comma-separated)
2. Do you want to find duplicates for a specific file type? (yes/no)
    - Enter the file extension (e.g., '.txt', '.jpg', '.pdf')

### Example Usage
```console
D:\dev\ExampleDirectory>python doop.py
Do you want to exclude any directories? (yes/no): yes
Enter the full paths of directories to exclude (comma-separated):
D:\dev\ExampleDirectory\Engine
Do you want to find duplicates for a specific file type? (yes/no): yes
Enter the file extension (e.g., '.txt', '.jpg', '.pdf'): .uasset

Duplicate files found for 'HealthActor_BP':
  [0] .\Testbed_Vcup\Plugins\Vcup\Content\Blueprints\HealthActor_BP.uasset
      Size: 22463 bytes
      Created: 2024-06-03 18:31:03.492919
      Modified: 2024-06-03 18:31:03.508876
  [1] .\VCMB_USJ\Plugins\Vcup\Content\Blueprints\HealthActor_BP.uasset
      Size: 22463 bytes
      Created: 2024-06-03 18:57:34.389077
      Modified: 2024-06-03 18:57:34.389077
Enter the numbers of files to delete (comma-separated, or 'skip'): skip
```
