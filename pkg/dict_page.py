class Page:
    def __init__(self, page_num, page_size, rec_list):
        """
        :param totalPage: 总页数
        :param recordCount: 总记录数
        :param page_num: 当前页
        :param pageSize:每页的数量
        """

        self.page_num = page_num
        self.page_size = page_size
        self.recordCount = len(rec_list)
        self.rec_list = rec_list
        self.totalPage, remainder = divmod(self.recordCount, self.page_size)
        if remainder:
            self.totalPage += 1
        self.set_datas()

    def set_datas(self):
        start_index = (self.page_num - 1) * self.page_size
        end_index = self.page_num * self.page_size
        self.datas = self.rec_list[start_index:end_index]
        del self.rec_list

    def get_str_json(self):
        # return str(self.__dict__).replace("'", "\"")
        return self.__dict__.get("datas")




