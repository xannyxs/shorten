use crate::livepeer::Livepeer;
use crate::video_processing::process_file;
use std::env;
use std::fs;
use std::path::Path;
use std::process;

mod livepeer;
mod structs;
mod upload_video;
mod video_processing;

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() != 2 {
        panic!("Program needs an argument");
    }

    if !Path::new("./credentials.json").exists() {
        panic!("Credentials file does not exist.");
    }

    if !Path::new("./.env.local").exists() {
        panic!(".env.local file does not exist.");
    }

    let livepeer = match env::var("LIVEPEER_API_KEY") {
        Ok(env) => Livepeer::new(env),
        Err(_e) => {
            println!("Cannot find LIVEPEER_API_KEY");
            process::exit(1);
        }
    };

    let path = Path::new(&args[1]);

    match fs::metadata(path) {
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
                                match process_file(&livepeer, &entry.path()).await {
                                    Ok(_) => println!("Succesfully uploaded video {:?}", path),
                                    Err(e) => eprintln!("{}", e),
                                };
                            }
                        }
                    }
                }
            } else {
                println!("Given path is a file");
                match process_file(&livepeer, &path).await {
                    Ok(_) => println!("Succesfully uploaded video {:?}", path),
                    Err(e) => eprintln!("{}", e),
                };
            }
        }
    }

    println!("Successfully completed program...");
}
