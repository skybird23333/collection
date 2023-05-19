const suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
/**
 * Convert a size to human readable format. Ripped from its Python counterpart
 * @param bytes The size in bytes to convert
 */
export default function humaniseSize(bytes: number): string {
    let i = 0
    while (bytes >= 1024 && i < suffixes.length - 1) {
        bytes /= 1024.
        i += 1
    }
    const size = bytes.toFixed(2)
    return`${size} ${suffixes[i]}`
}