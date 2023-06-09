use std::io;
use std::path::Path;
use std::process::{exit, Command};

pub fn call_python_script(video_path: &Path, asset_id: &str) -> io::Result<()> {
    let script_path = "/shorten/src/python/transcodeVideo.py";

    let output = Command::new("python3")
        .arg(&script_path)
        .arg(video_path)
        .arg(asset_id)
        .output()?;

    if !output.status.success() {
        return Err(io::Error::new(
            io::ErrorKind::Other,
            "Python script ended with error",
        ));
    }

    Ok(())
}
