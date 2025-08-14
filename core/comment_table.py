class CommentTable:

    class Comment:
        def __init__(self, pos: tuple[int, int]=(0,0), raw: str = r""):
            self.pos = pos      # tuple (line, column)
            self.raw = raw      # comment's text

        def __repr__(self):
            return f"Comment(pos={self.pos}, raw={self.raw})"

    def __init__(self):
        self.comments = []

    def add(self, pos: tuple[int, int], raw: str):
        comment = self.Comment(pos, raw)
        self.comments.append(comment)

    @staticmethod
    def set_place_holder(source: list[str],
                         line: int,
                         comment_num: int):
        holder = f"__COMMENT__{comment_num}"
        source[line] += f"    #{holder}"

    def __len__(self):
        return len(self.comments)

    def __getitem__(self, index: int):
        return self.comments[index]