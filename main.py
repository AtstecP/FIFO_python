class BufferDynamic:
    """
    Класс с динамическим списком
    Плюсы
    - Гибкость в размере: буфер может динамически увеличиваться или уменьшаться по мере
    того, как элементы помещаются в очередь или удаляются из очереди, приспосабливаясь к различным размерам данных.
    - Отсутствие потери памяти для неиспользуемых слотов: размер буфера регулируется динамически, что позволяет
    избежать необходимости выделения памяти для неиспользуемых слотов.

    Минусы
    - Накладные расходы на перераспределение памяти: когда буфер должен увеличиться за пределы своего текущего размера,
    происходит перераспределение памяти и копирование элементов, что в свою очередь затратно с точки зрения памяти и времени.
    -Производительность постановки и удаления из очереди: динамическое изменение размера буфера может привести к
    случайным перераспределениям ресурсов, влияющим на производительность операций постановки и удаления из очереди.
    """

    def __init__(self, max_size):
        self.__buffer = []
        self.__max_size = max_size
        self.__head = 0
        self.__tail = 0
        self.__size = 0

    def is_empty(self):
        return self.__size == 0

    def is_full(self):
        return self.__size == self.__max_size

    def enqueue(self, item):
        if self.is_full():
            raise Exception("Buffer is full")
        if len(self.__buffer) < self.__max_size:
            self.__buffer.append(item)
        else:
            self.__buffer[self.__tail] = item
        self.__tail = (self.__tail + 1) % self.__max_size
        self.__size += 1

    def dequeue(self):
        if self.is_empty():
            raise Exception("Buffer is empty")
        item = self.__buffer[self.__head]
        self.__buffer[self.__head] = None
        self.__head = (self.__head + 1) % self.__max_size
        self.__size -= 1
        return item

    def get_buffer(self):
        return self.__buffer


class BufferFixed:
    """
    Класс со списком фиксированного размера
    Плюсы
    - Эффективное использование памяти: поскольку размер буфера фиксирован,
    выделение памяти выполняется только один раз во время инициализации, что может быть полезно в средах с
    ограниченным объемом памяти.
    - Быстрая постановка в очередь и удаление из очереди: использование модульной
    арифметики для вычислений индекса делает операции постановки и удаления из очереди постоянным временем (O(1)),
    обеспечивая быстрый доступ к элементам буфера.

    Минусы
    - Ограниченная гибкость. Фиксированный размер буфера может быть ограничением, если количество элементов
    превышает размер буфера. В таких случаях может потребоваться дополнительная обработка или условия ошибки.
    - Неиспользуемая память для неиспользуемых слотов: если буфер не используется полностью, память, выделенная для
    неиспользуемых слотов, остается неиспользованной, что приводит к потенциальным потерям.
    """

    def __init__(self, max_size):
        self.__buffer = [None] * max_size
        self.__max_size = max_size
        self.__head = 0
        self.__tail = 0
        self.__size = 0

    def is_empty(self):
        return self.__size == 0

    def is_full(self):
        return self.__size == self.__max_size

    def enqueue(self, item):
        if self.is_full():
            raise Exception("Buffer is full")
        self.__buffer[self.__tail] = item
        self.__tail = (self.__tail + 1) % self.__max_size
        self.__size += 1

    def dequeue(self):
        if self.is_empty():
            raise Exception("Buffer is empty")
        item = self.__buffer[self.__head]
        self.__buffer[self.__head] = None
        self.__head = (self.__head + 1) % self.__max_size
        self.__size -= 1
        return item

    def get_buffer(self):
        return self.__buffer


class BufferFixedOverwrite:
    """
        Класс со списком фиксированного размера с возможностью переполнения
        Плюсы и минусы как в BufferFixed за одним дополнением. В этом классе создан подкласс итератора, который отслеживает
        очередь и дает возможность переполнять буфер при этом не нарушая очередь FIFO.
        """

    def __init__(self, max_size):
        self.__buffer = [None] * max_size
        self.__iter = self.Iterator(max_size - 1)
        self.__max_size = max_size
        self.__size = 0

    def is_full(self):
        return self.__size == self.__max_size

    def is_empty(self):
        return self.__size == 0

    def enqueue(self, item):
        self.__buffer[self.__iter.get_in()] = item
        self.__size += 1

    def dequeue(self):
        if not self.is_empty():
            out_index = self.__iter.get_out()
            element = self.__buffer[out_index]
            self.__buffer[out_index] = None
            self.__size -= 1
            return element
        else:
            return None

    def get_buffer(self):
        return f'{self.__buffer}  {self.__iter.get_val()} '

    class Iterator:
        """
        Класс итератор для контроля индекса записи и считывания.
        Даёт возможность переполгнения без потери очереди.
        """

        def __init__(self, max_index=1):
            self.max_index = max_index
            self.__in_index = 0
            self.__out_index = 0

        def get_val(self):
            return f'{self.__in_index} {self.__out_index}'

        def get_in(self):
            index = self.__in_index
            if self.__in_index != 0 and self.__in_index == self.__out_index:
                self.get_out()
            if self.__in_index == self.max_index:
                self.__in_index = 0
            else:
                self.__in_index += 1
            return index

        def get_out(self):
            index = self.__out_index
            if self.__out_index == self.max_index:
                self.__out_index = 0
            else:
                self.__out_index += 1
            return index


def main():
    pass


if __name__ == '__main__':
    main()
