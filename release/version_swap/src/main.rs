/// Helper script to swap old version/build numbers with new ones 
use std::fs;
use std::io::{self, BufRead, Write};

// Function to read the contents of a file into a vector of lines
fn read_file_lines(path: &str) -> io::Result<Vec<String>> {
    let file = fs::File::open(path)?;
    let reader = io::BufReader::new(file);
    reader.lines().collect()
}

// Function to write lines to a file
fn write_file_lines(path: &str, lines: &[String]) -> io::Result<()> {
    let mut file = fs::File::create(path)?;
    for line in lines {
        writeln!(file, "{}", line)?;
    }
    Ok(())
}

// Function to replace the version number in the setup.py
fn replace_setup_version(lines: &[String], new_version: &str) -> Vec<String> {
    lines
        .iter()
        .map(|line| {
            if line.trim().contains("version=") {
                let parts: Vec<&str> = line.split('"').collect();
                format!("{}\"{}\"{}", parts[0], new_version, parts[2])
            } else {
                line.clone()
            }
        })
        .collect()
}

// Function to replace the version number and build number in the defaults.py
fn replace_version_number(lines: &[String], new_version: &str, new_build_number: &str) -> Vec<String> {
    lines
        .iter()
        .map(|line| {
            if line.trim().contains("SDK_VERSION = ") {
                let parts: Vec<&str> = line.split('"').collect();
                format!("{}\"{}\" # v{}", parts[0], new_build_number, new_version)
            } else {
                line.clone()
            }
        })
        .collect()
}
fn main() -> io::Result<()> {
    let setup_file_path = "../../../setup.py";
    let defaults_file_path = "../../../src/onepassword/defaults.py";
    let version_file_path = "../../.version";
    let build_number_file_path = "../../.version-build";

    // Acquire setup.py and default.py file lines and updated version/build numbers
    let setup_lines = read_file_lines(setup_file_path)?;
    let default_lines = read_file_lines(defaults_file_path)?;
    let new_version = read_file_lines(version_file_path)?
        .get(0)
        .expect(".version should contain a version number")
        .trim()
        .to_string();

    let new_build_number = read_file_lines(build_number_file_path)?
        .get(0)
        .expect(".version-build is empty")
        .trim()
        .to_string();

    // Replace the version number in the setup.py file
    let updated_setup_lines = replace_setup_version(&setup_lines, &new_version);
    write_file_lines(setup_file_path, &updated_setup_lines)?;

    // Replace version number and build number in defaults.py
    let updated_defaults_lines = replace_version_number(&default_lines, &new_version, &new_build_number);
    write_file_lines(defaults_file_path, &updated_defaults_lines)?;

    Ok(())
}
