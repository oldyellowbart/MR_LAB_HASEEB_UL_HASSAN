# lab1_package_1

A small ROS 2 Python package created for Lab 1. This package provides a simple node that logs a welcome message and demonstrates an ament_python console script entry point.

## Summary

- Package name: `lab1_package_1`
- Entry point / executable: `my_node_1` -> `lab1_package_1.my_node_1:main`
- Purpose: minimal example ROS2 node used in lab exercises (logs a message then exits after a short spin)

## Requirements

- ROS 2 (Foxy / Galactic / Humble or later). Replace `<distro>` below with your installed distro name.
- Python 3
- colcon build tool (for building in a workspace)

## Quick start — build and run (recommended)

1. Open a terminal and source your ROS 2 installation:

```bash
source /opt/ros/<distro>/setup.bash
```

2. From the repository root (the folder that contains `week1`), change into the `week1` folder and build with colcon:

```bash
cd week1
colcon build --packages-select lab1_package_1
```

3. Source the local install overlay and run the node:

```bash
source install/setup.bash
ros2 run lab1_package_1 my_node_1
```

You should see a log message similar to "welcome to mobile robotics:0" printed to the console.

## Run directly (for quick debugging)

You can also run the node module directly (useful when iterating quickly):

```bash
python3 -m lab1_package_1.my_node_1
```

This runs the same `main()` entrypoint but bypasses ROS 2's `ros2 run` lookup — make sure your Python path includes the package (or run from the package root).

## What the node does

- File: `lab1_package_1/my_node_1.py`
  - Creates an `rclpy` Node named `lab1_node_test`.
  - Logs `welcome to mobile robotics:N` where `N` increments each time the module is imported/run.
  - Calls `rclpy.spin_once(node, timeout_sec=0.1)` and then exits cleanly.

This is intentionally minimal so you can expand it (publish/subscribe, timers, parameters, services) as lab tasks require.

## Files of interest

- `package.xml` — ROS package manifest (dependencies and metadata)
- `setup.py` — ament Python packaging settings; defines the console script entry point
- `lab1_package_1/my_node_1.py` — the node implementation and `main()`
- `test/` — automated tests present for flake8/pep257/copyright

## Running tests

This package includes test tooling configured via `setup.py` and the `test/` directory. To run tests locally:

```bash
# from week1 folder after building the workspace
colcon test --packages-select lab1_package_1
colcon test-result --verbose

# or run pytest directly (inside the package env)
pytest -q
```

Note: some tests are style/copyright checks (flake8/pep257). Ensure the Python files adhere to the project's style rules.

## Development notes / next steps

- Replace `TODO: Package description` and license fields in `package.xml` and `setup.py` with actual values.
- Add more functionality to `my_node_1.py` (publishers/subscribers, parameters) as needed for the lab.
- If you want the node to keep running, replace `spin_once` with `rclpy.spin(node)` and handle shutdown signals.

## Contributing

Open a PR with changes. Keep commit messages short and include tests for new behavior where applicable.

## License

Add a license of your choice to the repository and update `package.xml` and `setup.py` accordingly.

---

If you'd like, I can also:

- update the `package.xml` and `setup.py` TODO fields with suggested values (author, license, description), or
- add an example that publishes/subscribes so you have a fuller demo node.

Tell me which of those you'd like me to do next.
