from typing import Dict

class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # skip header
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0"""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {i: dataset[i] for i in range(len(dataset))}
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict:
        """Return a page of data that is resilient to deletions."""
        dataset = self.indexed_dataset()
        assert 0 <= index < len(self.__dataset), "Index out of range"

        data = []
        current_index = index
        collected = 0

        # Keep collecting items until we have page_size items
        while collected < page_size and current_index < len(dataset):
            if current_index in dataset:
                data.append(dataset[current_index])
                collected += 1
            current_index += 1

        next_index = current_index
        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data
        }
