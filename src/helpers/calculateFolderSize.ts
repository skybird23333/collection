import type { VaultDocument } from "@/types/interfaces"

/**
 * Recursively calculate the entire size of a folder. Probably isn't the best implementation but we will see.
 * @param folder Folder data, same format as the index.json
 */
export default function calculateFolderSize(folder: { [key: string] : any | VaultDocument }): number {
    let totalSize = 0
    for (const [key, value] of Object.entries(folder)) {
        if(value.size && value.name) { //Value is a document
            totalSize += value.size
        } else { //Value is another document
            totalSize += calculateFolderSize(value)
        }
    }

    return totalSize
}