import os
import hashlib

def create_partition_image(partition_path, output_image_file, chunk_size=1024*1024):
    md5_hash = hashlib.md5()
    total_bytes = 0

    try:
        with open(partition_path, 'rb') as part, open(output_image_file, 'wb') as image_file:
            while True:
                chunk = part.read(chunk_size)
                if not chunk:
                    break
                image_file.write(chunk)
                md5_hash.update(chunk)
                total_bytes += len(chunk)
                print(f"\rRead {total_bytes/(1024*1024):.2f} MB", end='')
    except PermissionError:
        print("Permission denied. Run as Administrator.")
        return False
    except Exception as e:
        print(f"\nError: {e}")
        return False

    print("\nPartition image creation completed.")
    print("MD5 Hash of image:", md5_hash.hexdigest())
    return True

if __name__ == "__main__":
    drive_letter = input("Enter the drive letter to image (e.g. C, D, E,F,G): ").upper().strip()
    if len(drive_letter) != 1 or not drive_letter.isalpha():
        print("Invalid drive letter entered. Exiting.")
        exit(1)

    partition = f"\\\\.\\{drive_letter}:"  # Windows raw device path
    output_file = f"partition_image_{drive_letter}.img"

    print(f"Starting partition image creation from {partition} to {output_file}...")
    success = create_partition_image(partition, output_file)

    if success:
        print(f"Partition image created successfully: {output_file}")
    else:
        print("Partition image creation failed.")