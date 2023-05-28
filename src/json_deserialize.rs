use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub(crate) struct Asset {
    pub(crate) id: String,
    playbackId: String,
    userId: String,
    createdAt: u64,
    status: Status,
    name: String,
    source: Source,
}

#[derive(Serialize, Deserialize, Debug)]
struct Status {
    phase: String,
    updatedAt: u64,
}

#[derive(Serialize, Deserialize, Debug)]
struct Source {
    #[serde(rename = "type")]
    type_: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct Task {
    id: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub(crate) struct Response {
    pub(crate) url: String,
    tusEndpoint: String,
    pub(crate) asset: Asset,
    task: Task,
}
