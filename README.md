Spigt
SPIGT (Simple Patch Install and Generate Tool) is a versatile tool designed to facilitate the installation and generation of patches for software that supports SPIGT. This tool ensures that the patching process is both efficient and straightforward.

Software Requirements
For a software to be compatible with SPIGT, it must include the following files:

version.json: Contains the version number of the software.
{
  "ver": "versionNumber"
}

.spt (name can be any string): An empty file that signifies the software's compatibility with SPIGT.
Usage
SPIGT offers two primary functions: install and generate.

Install Function   
The install function is used to apply a patch to a software directory. Here’s how it works:install

Provide a Patch File: The patch file must be in .csp format.
Specify the Software Directory: Input the path to the directory where your software is installed.
Start the Installation: Click "Start" to begin the installation process.
Important: The patch must be compatible with the version of your software as specified in version.json. If the patch is not compatible, an error message (Err: The software is not supported by Spigt.) will be displayed.

Generate Function
The generate function creates patch files based on differences between software versions. Here’s how it works:

Upload Directories: You need to upload at least two directories:
One directory containing the latest version of the software.
One or more directories containing previous versions (pre-versions) of the software.
Select Output Format: You can choose to generate either:
A single patch file containing updates for all uploaded pre-versions.
Multiple patch files, each containing updates for a specific pre-version.
Warning: If you upload more than 10 pre-versions and choose to generate a single patch file, a warning will be issued:

Warning: You've uploaded more than 10 supported pre-versions and the resulting files can be very bloated, are you sure?

Start Generation: After setting your preferences, click "Start" to begin the generation process. The tool will:

Identify common elements between the directories.
Determine the differences to create update information.
Compress the update information into a .csp (compressed simple patch) file.
Example of Update Information
The update information might look like this:

{
    "ver1.7":{
        "main.exe":[
            {
                "action":"add",
                "location":0,
                "charactor":"//This is a file\n"
            },
            {
                "action":"delete",
                "location":[1,2],
                "charactor":null
            },
            {
                "action":"replace",
                "location":[3,16],
                "charactor":"MessageBox.Show(\"Error:Syntax Error\");\n"
            }
        ]
    }
}

It is in JSON format, and the extension is only used to distinguish functions.

Conclusion
SPIGT simplifies the process of managing software patches, ensuring that updates are applied accurately and efficiently. Whether you are installing a patch or generating one, SPIGT provides the necessary tools to streamline your workflow.
