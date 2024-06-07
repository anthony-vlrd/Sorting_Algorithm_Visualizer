import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Class to handle drawing and displaying information
class Drawinfo:
    # Color definitions
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE 

    # Gradients for the bars
    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    # Fonts for display
    FONT = pygame.font.SysFont('comicsans', 20)
    ALGO_FONT = pygame.font.SysFont('comicsans', 15)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)

    # Padding for the drawing area
    SIDE_PAD = 100
    TOP_PAD = 150

    # Initialize the drawing info with width, height, and list to sort
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    # Set the list and calculate properties for drawing the bars
    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

# Draw the entire screen including title, controls, and list bars
def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.RED)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))

    sorting = draw_info.ALGO_FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | M - Merge Sort | Q - Quick Sort | H - Heap Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))

    draw_list(draw_info)
    pygame.display.update()

# Draw the list bars on the screen
def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()

# Create a random starting list of numbers
def create_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

# Function for Bubble Sort Algorithm 
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst

# Function for Insertion Sort Algorithm 
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst

# Function for Selection Sort Algorithm 
def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)):
        min_idx = i
        for j in range(i + 1, len(lst)):
            if (lst[j] < lst[min_idx] and ascending) or (lst[j] > lst[min_idx] and not ascending):
                min_idx = j
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, min_idx: draw_info.RED}, True)
        yield True

    return lst

# Function for Merge Sort Algorithm 
def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def merge_sort_helper(lst, l, r, draw_info, ascending):
        if l >= r:
            return

        mid = (l + r) // 2
        yield from merge_sort_helper(lst, l, mid, draw_info, ascending)
        yield from merge_sort_helper(lst, mid + 1, r, draw_info, ascending)
        yield from merge(lst, l, mid, r, draw_info, ascending)
        draw_list(draw_info, {i: draw_info.GREEN for i in range(l, r + 1)}, True)
        yield True

    def merge(lst, l, mid, r, draw_info, ascending):
        left = lst[l:mid + 1]
        right = lst[mid + 1:r + 1]

        i = j = 0
        k = l

        while i < len(left) and j < len(right):
            if (left[i] < right[j] and ascending) or (left[i] > right[j] and not ascending):
                lst[k] = left[i]
                i += 1
            else:
                lst[k] = right[j]
                j += 1
            k += 1
            draw_list(draw_info, {k: draw_info.RED}, True)
            yield True

        while i < len(left):
            lst[k] = left[i]
            i += 1
            k += 1
            draw_list(draw_info, {k: draw_info.RED}, True)
            yield True

        while j < len(right):
            lst[k] = right[j]
            j += 1
            k += 1
            draw_list(draw_info, {k: draw_info.RED}, True)
            yield True

    yield from merge_sort_helper(lst, 0, len(lst) - 1, draw_info, ascending)

    return lst

# Function for Quick Sort Algorithm
def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def quick_sort_helper(lst, low, high, draw_info, ascending):
        if low < high:
            pi = yield from partition(lst, low, high, draw_info, ascending)
            yield from quick_sort_helper(lst, low, pi - 1, draw_info, ascending)
            yield from quick_sort_helper(lst, pi + 1, high, draw_info, ascending)

    def partition(lst, low, high, draw_info, ascending):
        pivot = lst[high]
        i = low - 1
        for j in range(low, high):
            if (lst[j] < pivot and ascending) or (lst[j] > pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED, high: draw_info.BLACK}, True)
                yield True
        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        draw_list(draw_info, {i + 1: draw_info.GREEN, high: draw_info.RED}, True)
        yield True
        return i + 1

    yield from quick_sort_helper(lst, 0, len(lst) - 1, draw_info, ascending)

    return lst

# Function for Heap Sort Algorithm
def heap_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def heapify(lst, n, i, draw_info, ascending):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and ((lst[i] < lst[l] and ascending) or (lst[i] > lst[l] and not ascending)):
            largest = l

        if r < n and ((lst[largest] < lst[r] and ascending) or (lst[largest] > lst[r] and not ascending)):
            largest = r

        if largest != i:
            lst[i], lst[largest] = lst[largest], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, largest: draw_info.RED}, True)
            yield True
            yield from heapify(lst, n, largest, draw_info, ascending)

    n = len(lst)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(lst, n, i, draw_info, ascending)

    for i in range(n - 1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, 0: draw_info.RED}, True)
        yield True
        yield from heapify(lst, i, 0, draw_info, ascending)

    return lst

# Main function
def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = create_starting_list(n, min_val, max_val)
    draw_info = Drawinfo(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(90)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = create_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algo_name = "Heap Sort"

    pygame.quit()

# Run the main function
if __name__ == "__main__":
    main()
