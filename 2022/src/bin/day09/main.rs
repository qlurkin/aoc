#[derive(Debug, Clone)]
struct Position(i32, i32);

#[derive(Debug, Clone)]
enum Move {
    R,
    L,
    U,
    D,
}

impl Move {
    fn from(txt: &str) -> Self {
       if txt == "R" { Move::R } 
       else if txt == "L" { Move::L } 
       else if txt == "U" { Move::U } 
       else if txt == "D" { Move::D } 
       else {
           panic!("Unknown Move: {}", txt)
       }
    }
}

fn load_data() -> Vec<Move> {
    let content = include_str!("test");
    content
        .split('\n')
        .flat_map(|line| {
            let mut it = line.split(' ');
            if let Some(direction) = it.next() {
                if let Some(count) = it.next() {
                    return std::iter::repeat(direction).take(count.parse::<usize>().unwrap());
                }
            }
            std::iter::repeat("").take(0)
        })
        .map(Move::from)
        .collect()
}

fn main() {
    let mut rope: Vec<Position> = std::iter::repeat(Position(0, 0)).take(10).collect();
    let moves = load_data();

    moves.iter().for_each(|mov| {
        match mov {
            Move::R => { rope[0] = Position(rope[0].0, rope[0].1 + 1) }
            Move::L => { rope[0] = Position(rope[0].0, rope[0].1 - 1) }
            Move::U => { rope[0] = Position(rope[0].0 - 1, rope[0].1) }
            Move::D => { rope[0] = Position(rope[0].0 + 1, rope[0].1) }
        }
    });
}
