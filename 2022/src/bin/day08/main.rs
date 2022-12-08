use std::ops;

#[derive(Debug)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[derive(Clone, Debug)]
struct Position {
    line: i32,
    column: i32,
}

struct Grid {
    width: usize,
    height: usize,
    items: Vec<u8>,
}

impl Grid {
    fn get(&self, position: &Position) -> Option<u8> {
        if (position.line < 0) || (position.line >= self.height as i32) || (position.column < 0) || (position.column >= self.width as i32) {
            return None
        }

        let index = position.line * self.width as i32 + position.column;
        Some(self.items[index as usize])
    } 
}


impl ops::Add<&Position> for &Position {
    type Output = Position;
    fn add(self, rhs: &Position) -> Position {
        Position { line: self.line + rhs.line, column: self.column + rhs.column } 
    }
}

impl ops::Add<&Direction> for &Position {
    type Output = Position;
    fn add(self, rhs: &Direction) -> Position {
        match rhs {
            Direction::Up => Position { line: self.line - 1, column: self.column },
            Direction::Down => Position { line: self.line + 1, column: self.column },
            Direction::Left => Position { line: self.line, column: self.column - 1 },
            Direction::Right => Position { line: self.line, column: self.column + 1 },
        }
    }
}

fn is_outside(position: Position, width: i32, height: i32) -> bool {
    (position.line < 0) || (position.line >= height) || (position.column < 0) || (position.column >= width) 
}

fn is_visible_from(grid: &Grid, position: &Position, direction: &Direction) -> bool {
    if let Some(start_height) = grid.get(&position) {
        let mut position = (*position).to_owned();
        while let Some(tree_height) = grid.get(&position) {
            if tree_height >= start_height {
                return false;
            }
            position = &position + direction;
        }
        return true;
    }
    else {
        panic!("No tree at this position {:?}", position);
    }
}

fn is_visible(grid: &Grid, position: &Position) -> bool {
    if is_visible_from(&grid, &position, &Direction::Up) {
       true 
    }
    else if is_visible_from(&grid, &position, &Direction::Up) {
       true 
    }
    else if is_visible_from(&grid, &position, &Direction::Up) {
       true 
    }
    else if is_visible_from(&grid, &position, &Direction::Up) {
       true 
    }
    else {
        false
    }
}

fn parse() {

}

fn main() {

}
