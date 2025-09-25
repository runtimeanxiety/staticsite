def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        lines = block.split("\n")
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line != "":
                cleaned_lines.append(line)
        if cleaned_lines:
            blocks.append("\n".join(cleaned_lines))
    return blocks