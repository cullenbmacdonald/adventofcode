use std::{fs::read_to_string, error::Error};

fn process_file() -> Result<(Vec<u32>, Vec<u32>), Box<dyn Error>> {
    let content = read_to_string("input.txt")?; // Store the string in a variable
    let lines = content.lines(); // Use the lines iterator

    let (mut left, mut right): (Vec<u32>, Vec<u32>) = lines
        .map(|line| {
            let mut parts = line.split_whitespace();
            let l = parts.next().ok_or("Missing left value")?.parse::<u32>()?;
            let r = parts.next().ok_or("Missing right value")?.parse::<u32>()?;
            Ok((l, r))
        })
        .collect::<Result<Vec<_>, Box<dyn Error>>>()?
        .into_iter()
        .unzip();

    left.sort_unstable();
    right.sort_unstable();

    Ok((left, right))
}

fn solve_01(left: &[u32], right: &[u32]) -> u32 {
    left.iter().zip(right).map(|(a, b)| {
        a.abs_diff(*b)
    }).sum()
}

fn main() -> Result<(), Box<dyn Error>> {
    let (left, right) = process_file()?;

    println!("{}", solve_01(&left, &right));
    Ok(())
}
