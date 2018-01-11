from PCPartPicker_API import PCPartPicker

print("Total CPU pages:", PCPartPicker.get_total_pages("cpu"))

# Gets info on page 2
cpu_info = PCPartPicker.get_part("cpu", 2)

# Print the names of all the CPUs on page 2
for cpu in cpu_info:
    print(cpu["name"], ":", cpu["price"])
