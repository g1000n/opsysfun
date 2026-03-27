# =========================================================
# PAGED REPLACEMENT SIMULATION PROJECT
# Algorithms Included:
# 1. FIFO
# 2. LRU
# 3. MRU
# 4. OPTIMAL
# 5. SECOND CHANCE
# =========================================================

def parse_reference_string(ref_input):
    return [int(x) for x in ref_input.strip().split()]


def calculate_rates(total_references, page_faults):
    page_hits = total_references - page_faults
    failure_rate = (page_faults / total_references) * 100 if total_references > 0 else 0
    success_rate = (page_hits / total_references) * 100 if total_references > 0 else 0
    return page_hits, failure_rate, success_rate


def record_step(steps, step_number, page, frames, num_frames, result):
    display_frames = frames[:] + ["-"] * (num_frames - len(frames))
    steps.append({
        "step": step_number,
        "page": page,
        "frames": display_frames,
        "result": result
    })


def print_results(algorithm_name, reference_string, num_frames, steps, page_faults):
    total_references = len(reference_string)
    page_hits, failure_rate, success_rate = calculate_rates(total_references, page_faults)

    print("\n" + "=" * 90)
    print(f"Algorithm: {algorithm_name}")
    print(f"Number of Pages: {total_references}")
    print(f"Number of Frames: {num_frames}")
    print("Page Reference String:", " ".join(map(str, reference_string)))
    print("=" * 90)

    header = ["Step", "Page"] + [f"Frame{i+1}" for i in range(num_frames)] + ["Result"]
    print(f"{header[0]:<8}{header[1]:<8}", end="")
    for i in range(num_frames):
        print(f"{header[i+2]:<10}", end="")
    print(f"{header[-1]:<10}")

    print("-" * 90)

    for step in steps:
        print(f"{step['step']:<8}{step['page']:<8}", end="")
        for frame_value in step["frames"]:
            print(f"{str(frame_value):<10}", end="")
        print(f"{step['result']:<10}")

    print("-" * 90)
    print(f"Total Page Faults (Failures): {page_faults}")
    print(f"Total Page Hits (Successes): {page_hits}")
    print(f"Failure Rate: {failure_rate:.2f}%")
    print(f"Success Rate: {success_rate:.2f}%")
    print("=" * 90)


# =========================================================
# FIFO
# =========================================================
def fifo(reference_string, num_frames):
    frames = []
    pointer = 0
    page_faults = 0
    steps = []

    for i, page in enumerate(reference_string, start=1):
        if page in frames:
            result = "Hit"
        else:
            result = "Fault"
            page_faults += 1

            if len(frames) < num_frames:
                frames.append(page)
            else:
                frames[pointer] = page
                pointer = (pointer + 1) % num_frames

        record_step(steps, i, page, frames, num_frames, result)

    return steps, page_faults


# =========================================================
# LRU
# =========================================================
def lru(reference_string, num_frames):
    frames = []
    last_used = {}
    page_faults = 0
    steps = []

    for i, page in enumerate(reference_string, start=1):
        if page in frames:
            result = "Hit"
        else:
            result = "Fault"
            page_faults += 1

            if len(frames) < num_frames:
                frames.append(page)
            else:
                least_recently_used = min(frames, key=lambda p: last_used[p])
                replace_index = frames.index(least_recently_used)
                frames[replace_index] = page

        last_used[page] = i
        record_step(steps, i, page, frames, num_frames, result)

    return steps, page_faults


# =========================================================
# MRU
# =========================================================
def mru(reference_string, num_frames):
    frames = []
    last_used = {}
    page_faults = 0
    steps = []

    for i, page in enumerate(reference_string, start=1):
        if page in frames:
            result = "Hit"
        else:
            result = "Fault"
            page_faults += 1

            if len(frames) < num_frames:
                frames.append(page)
            else:
                most_recently_used = max(frames, key=lambda p: last_used[p])
                replace_index = frames.index(most_recently_used)
                frames[replace_index] = page

        last_used[page] = i
        record_step(steps, i, page, frames, num_frames, result)

    return steps, page_faults


# =========================================================
# OPTIMAL
# =========================================================
def optimal(reference_string, num_frames):
    frames = []
    page_faults = 0
    steps = []

    for i, page in enumerate(reference_string, start=1):
        current_index = i - 1

        if page in frames:
            result = "Hit"
        else:
            result = "Fault"
            page_faults += 1

            if len(frames) < num_frames:
                frames.append(page)
            else:
                next_use = {}

                for frame_page in frames:
                    if frame_page in reference_string[current_index + 1:]:
                        future_index = reference_string[current_index + 1:].index(frame_page)
                        next_use[frame_page] = future_index
                    else:
                        next_use[frame_page] = float("inf")

                page_to_replace = max(next_use, key=next_use.get)
                replace_index = frames.index(page_to_replace)
                frames[replace_index] = page

        record_step(steps, i, page, frames, num_frames, result)

    return steps, page_faults


# =========================================================
# SECOND CHANCE
# =========================================================
def second_chance(reference_string, num_frames):
    frames = []
    reference_bits = []
    pointer = 0
    page_faults = 0
    steps = []

    for i, page in enumerate(reference_string, start=1):
        if page in frames:
            result = "Hit"
            page_index = frames.index(page)
            reference_bits[page_index] = 1
        else:
            result = "Fault"
            page_faults += 1

            if len(frames) < num_frames:
                frames.append(page)
                reference_bits.append(1)
            else:
                while True:
                    if reference_bits[pointer] == 0:
                        frames[pointer] = page
                        reference_bits[pointer] = 1
                        pointer = (pointer + 1) % num_frames
                        break
                    else:
                        reference_bits[pointer] = 0
                        pointer = (pointer + 1) % num_frames

        record_step(steps, i, page, frames, num_frames, result)

    return steps, page_faults


# =========================================================
# MENU DISPLAY
# =========================================================
def display_menu():
    print("\n" + "=" * 50)
    print("PAGED REPLACEMENT SIMULATION")
    print("=" * 50)
    print("1. FIFO")
    print("2. LRU")
    print("3. MRU")
    print("4. OPTIMAL")
    print("5. SECOND CHANCE")
    print("6. Run All Algorithms")
    print("7. Exit")
    print("=" * 50)


# =========================================================
# USER INPUT
# =========================================================
def get_user_input():
    while True:
        try:
            num_frames = int(input("Enter number of frames: "))
            if num_frames <= 0:
                print("Number of frames must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:
        try:
            ref_input = input("Enter page reference string (space-separated): ")
            reference_string = parse_reference_string(ref_input)
            if len(reference_string) == 0:
                print("Reference string cannot be empty.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter integers only, separated by spaces.")

    return num_frames, reference_string


# =========================================================
# MAIN PROGRAM
# =========================================================
def main():
    while True:
        display_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "7":
            print("Exiting program...")
            break

        if choice not in ["1", "2", "3", "4", "5", "6"]:
            print("Invalid choice. Please choose from 1 to 7.")
            continue

        num_frames, reference_string = get_user_input()

        if choice == "1":
            steps, faults = fifo(reference_string, num_frames)
            print_results("FIFO", reference_string, num_frames, steps, faults)

        elif choice == "2":
            steps, faults = lru(reference_string, num_frames)
            print_results("LRU", reference_string, num_frames, steps, faults)

        elif choice == "3":
            steps, faults = mru(reference_string, num_frames)
            print_results("MRU", reference_string, num_frames, steps, faults)

        elif choice == "4":
            steps, faults = optimal(reference_string, num_frames)
            print_results("OPTIMAL", reference_string, num_frames, steps, faults)

        elif choice == "5":
            steps, faults = second_chance(reference_string, num_frames)
            print_results("SECOND CHANCE", reference_string, num_frames, steps, faults)

        elif choice == "6":
            algorithms = [
                ("FIFO", fifo),
                ("LRU", lru),
                ("MRU", mru),
                ("OPTIMAL", optimal),
                ("SECOND CHANCE", second_chance)
            ]

            for name, algorithm_function in algorithms:
                steps, faults = algorithm_function(reference_string, num_frames)
                print_results(name, reference_string, num_frames, steps, faults)


if __name__ == "__main__":
    main()