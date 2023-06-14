use std::io;
use std::path::Path;
use std::process::Command;
use std::str;

pub fn call_python_script(video_path: &Path, asset_id: &str) -> io::Result<()> {
    let script_path = "/shorten/src/python/transcodeVideo.py";

    println!("Staring Python script");
    let output = Command::new("python3")
        .arg(script_path)
        .arg(video_path)
        .arg(asset_id)
        .output()?;

    if !output.status.success() {
        let stderr =
            str::from_utf8(&output.stderr).unwrap_or("Failed to parse python script stderr output");
        let stdout =
            str::from_utf8(&output.stdout).unwrap_or("Failed to parse python script stdout output");

        return Err(io::Error::new(
            io::ErrorKind::Other,
            format!(
                "Python script ended with error:\nStderr:\n{}\nStdout:\n{}",
                stderr, stdout
            ),
        ));
    }

    Ok(())
}
