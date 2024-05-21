hello = "hello,"
world = "world"
print(hello, world)

def find_squares(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Step 1: Dynamic programming to find the largest square ending at each point
    dp = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1

    # Step 2: Greedily find squares to cover the black parts
    squares = []
    covered = [[False] * cols for _ in range(rows)]

    def is_covered(x, y, size):
        for i in range(x, x + size):
            for j in range(y, y + size):
                if not (0 <= i < rows and 0 <= j < cols and grid[i][j] == 1 and not covered[i][j]):
                    return False
        return True

    def cover(x, y, size):
        for i in range(x, x + size):
            for j in range(y, y + size):
                covered[i][j] = True

    for i in reversed(range(rows)):
        for j in reversed(range(cols)):
            if grid[i][j] == 1 and not covered[i][j]:
                size = dp[i][j]
                while size > 0 and not is_covered(i - size + 1, j - size + 1, size):
                    size -= 1
                if size > 0:
                    squares.append([i - size + 1, j - size + 1, size])
                    cover(i - size + 1, j - size + 1, size)

    return squares

# Example usage
grid = [
    [1, 1, 0, 1],
    [1, 1, 1, 1],
    [0, 1, 1, 1],
    [0, 1, 1, 1]
]

print(find_squares(grid))  # Output: [[0, 0, 2], [0, 3, 1], [1, 1, 3]]