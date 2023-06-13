use crate::livepeer::Livepeer;
use crate::video_processing::process_file;
use io::Result;
use std::path::Path;
use std::{env, io};

mod livepeer;
mod structs;
mod upload_video;
mod video_processing;
use walkdir::WalkDir;

fn assert_argument_count(args: &[String]) {
    if args.len() != 2 {
        panic!("Program needs an argument");
    }
}

fn assert_file_exists(path: &str) {
    if !Path::new(path).exists() {
        panic!("{} file does not exist.", path);
    }
}

fn get_livepeer_api_key() -> Livepeer {
    let livepeer_key = env::var("LIVEPEER_API_KEY").expect("Cannot find LIVEPEER_API_KEY");
    Livepeer::new(livepeer_key)
}

async fn handle_directory(livepeer: &Livepeer, root_path: &Path) -> Result<()> {
    for entry in WalkDir::new(root_path)
        .into_iter()
        .filter_map(|e| e.ok()) // Handles walkdir::Error
        .filter(|e| !e.file_type().is_dir())
    {
        let path = entry.path();
        match process_file(livepeer, path).await {
            Ok(_) => println!("Successfully uploaded video {:?}", path),
            Err(e) => eprintln!("{}", e),
        }
    }
    Ok(())
}

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();

    assert_argument_count(&args);
    assert_file_exists("./credentials.json");
    assert_file_exists("./.env.local");

    let livepeer = get_livepeer_api_key();
    let path = Path::new(&args[1]);

    handle_directory(&livepeer, path)
        .await
        .unwrap_or_else(|e| panic!("Error while handling directory: {}", e));

    println!("Successfully completed program...");
}
