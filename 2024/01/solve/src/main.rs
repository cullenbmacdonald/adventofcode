use std::{fs::read_to_string, iter::zip, path::absolute};

fn process_file() -> (Vec<u32>, Vec<u32>) {
    let mut left = Vec::<u32>::new();
    let mut right = Vec::<u32>::new();
    let lines: Vec<String> = read_to_string("input.txt")
        .unwrap()
        .lines()
        .map(String::from)
        .collect();

    for line in lines {
        let split: Vec<&str> = line.split_whitespace().collect();
        left.push(split[0].parse::<u32>().unwrap());
        right.push(split[1].parse::<u32>().unwrap());
    }
    left.sort();
    right.sort();
    (left, right)
}

fn solve_01(left: Vec<u32>, right: Vec<u32>) -> u32 {
    left.iter().zip(right).map(|(a, b)| {
        println!("{} {}", a, b);
        a.abs_diff(b)
    }).sum()
}

fn main() {
    let (left, right) = process_file();

    println!("{}", solve_01(left, right));
}
