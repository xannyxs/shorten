use crate::livepeer::Livepeer;
use crate::video_processing::process_file;
use std::env;
use std::fs;
use std::path::Path;
use std::process;

mod json_deserialize;
mod livepeer;
mod upload_video;
mod video_processing;

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() != 2 {
        eprintln!("Program needs an argument");
        process::exit(1);
    }

    if !Path::new("./credentials.json").exists() {
        eprintln!("Credentials file does not exist.");
        process::exit(1);
    }

    if !Path::new("./.env.local").exists() {
        eprintln!(".env.local file does not exist.");
        process::exit(1);
    }

    let livepeer = match env::var("LIVEPEER_API_KEY") {
        Ok(env) => Livepeer::new(env),
        Err(_e) => {
            println!("Cannot find LIVEPEER_API_KEY");
            process::exit(1);
        }
    };

    let path = Path::new(&args[1]);

    match fs::metadata(&path) {
        Err(e) => {
            eprintln!("{}", e);
            process::exit(1);
        }
        Ok(metadata) => {
            if metadata.is_dir() {
                println!("Given path is a directory");
                match fs::read_dir(path) {
                    Err(e) => {
                        eprintln!("A fatal error happened: {}", e);
                        process::exit(1);
                    }
                    Ok(entries) => {
                        for entry in entries {
                            let entry = entry.unwrap();
                            if entry.metadata().unwrap().is_file() {
                                video_processing::process_file(&livepeer, &entry.path());
                            }
                        }
                    }
                }
            } else {
                println!("Given path is a file");
                process_file(&livepeer, &path).await;
            }
        }
    }

    println!("Successfully completed program...");
}
