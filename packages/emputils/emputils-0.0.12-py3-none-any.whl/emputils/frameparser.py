import re
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import sys
from datetime import datetime


class Word:
    def __init__(self, word_string):
        self.string = word_string
        self.header = int(self.string[0], 16)
        self.body = self.string[2:]
        self.value = int(self.body, 16) if self.header != 0 else 0

    def isValid(self):
        return (self.header != 0)

    def __str__(self):
        return str(self.string)

    def getValue(self):
        return self.value


class Frame:
    def __init__(self, line):
        self.line = line
        self.words = []
        self.parse()

    def parse(self):
        reg = re.match("Frame [0-9]* :", self.line)
        if reg:
            self.number = int(reg.group().split(" ")[1])
        else:
            self.number = None
        word_strings = self.line.split(":")[1].split(" ")
        self.words = [Word(i) for i in word_strings if i]

    def validMask(self):
        return [word.isValid() for word in self.words]

    def getValues(self):
        return [word.getValue() for word in self.words]

    def __len__(self):
        if len(self.words) == 0:
            self.parse()
        return len(self.words)

    def __str__(self):
        return str(self.line)


class Buffer:
    def __init__(self, filename=None, alignment_map=None):
        self.header, self.frames, self.mask, self.values = [], [], [], []
        self.filename = filename
        if (filename is not None):
            self.openFile(filename)
        self.alignment_map = alignment_map
        self.aligned = False

    def openFile(self, filename):
        self.lines = [line.strip() for line in open(filename)]
        self.stripHeader()

    def stripHeader(self):
        if len(self.header) == 0:
            for i in range(3):
                self.header.append(self.lines.pop(0))
        for line in self.header:
            if line.startswith("Link"):
                self.links = [
                    int(i) for i in line.split(':')[1].split(" ") if i]

    def getFrames(self):
        if (len(self.header) == 0):
            self.stripHeader()
        self.frames = [Frame(line) for line in self.lines]
        return self.frames

    def getDataFrame(self, data_type='values'):
        self.getFrames()
        if self.aligned is False and self.alignment_map is not None:
            aligned_links = [0 for i in range(len(self.links))]
            for pair in self.alignment_map.values:
                if pair[1] in self.links:
                    index = self.links.index(pair[1])
                    aligned_links[index] = pair[0]
            self.links = aligned_links
            self.aligned = True
        if data_type == 'valid':
            values = np.array(
                [frame.validMask() for frame in self.frames], dtype=int)
        elif data_type == 'values':
            values = np.array(
                [frame.getValues() for frame in self.frames], dtype=int)
        else:
            return
        df = pd.DataFrame(values, columns=self.links)
        return df.sort_index(axis=1)

    def stripEmpty(self):
        if (len(self.frames) == 0):
            self.getFrames()
        for i in range(len(self.frames) - 1, -1, -1):
            if sum(self.frames[i].validMask()) == 0:
                self.frames.pop(i)

    def getValidWindow(self):
        if len(self.mask == 0):
            self.mask = self.getDataFrame(data_type='valid').values
        mask = self.mask == 0
        rows = np.flatnonzero((~mask).sum(axis=1))
        cols = np.flatnonzero((~mask).sum(axis=0))
        m = self.mask[rows.min():rows.max()+1, cols.min():cols.max()+1]
        return rows, cols, (m != 0).argmax(axis=0)

    def flattenLinkOffset(self, data, offsets):
        values = np.zeros(data.shape)
        for i in range(len(offsets)):
            values[:len(data)-offsets[i], i] = data[offsets[i]:, i]
        return values

    def plotMask(self, ax, remove_empty='both'):
        self.mask = self.getDataFrame(data_type='valid').values
        rows, cols, offsets = self.getValidWindow()
        self.mask = self.mask[rows.min():rows.max()+1, cols.min():cols.max()+1]
        self.mask = self.flattenLinkOffset(self.mask, offsets)
        ax.imshow(self.mask, aspect='auto', cmap='hot')

    def plotValues(self, ax, remove_empty='both'):
        self.values = self.getDataFrame(data_type='values').values
        rows, cols, offsets = self.getValidWindow()
        self.values = self.values[
            rows.min():rows.max()+1, cols.min():cols.max()+1]
        self.values = self.flattenLinkOffset(self.values, offsets)
        ax.imshow(self.values, aspect='auto', cmap='hot')


def compareBufferMasks(buffer1, buffer2):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
    fig.suptitle('Output buffer comparison')
    buffer1.plotMask(ax1)
    ax1.set_title("Buffer #1")
    ax1.set_ylabel("Frame")
    ax1.set_xlabel("Link")
    ax1.set_xticklabels(buffer1.links)
    buffer2.plotMask(ax2)
    ax2.set_title("Buffer #2")
    ax2.set_xlabel("Link")
    ax2.set_xticklabels(buffer2.links)
    if len(buffer1.mask) < len(buffer2.mask):
        diff_mask = abs(buffer1.mask - buffer2.mask[:len(buffer1.mask)])
    else:
        diff_mask = abs(buffer1.mask[:len(buffer2.mask)] - buffer2.mask)
    ax3.imshow(diff_mask, aspect='auto')
    print("Accuracy: %0.4f" % (1-np.sum(diff_mask)/diff_mask.size))
    ax3.set_title("Comparison")
    ax3.set_xlabel("Link")
    ax3.set_xticklabels(buffer1.links)
    time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    plt.savefig(time + "_mask_comparison.png", dpi=500)


def plotBuffer(buffer):
    fig, ax = plt.subplots(1, 1)
    buffer.plotMask(ax)
    ax.set_ylabel("Frame")
    ax.set_xlabel("Link")
    ax.set_xticklabels(buffer.links)
    filename = buffer.filename.split(".")[0] + ".png"
    plt.savefig(filename, dpi=500)
    plt.show()


def deepInspect(buffer1, buffer2):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
    fig.suptitle('Output buffer comparison')
    buffer1.plotValues(ax1)
    ax1.set_title("Buffer #1")
    ax1.set_ylabel("Frame")
    ax1.set_xlabel("Link")
    ax1.set_xticklabels(buffer1.links)
    buffer2.plotValues(ax2)
    ax2.set_title("Buffer #2")
    ax2.set_xlabel("Link")
    ax2.set_xticklabels(buffer2.links)
    if len(buffer1.values) < len(buffer2.values):
        diff_values = abs(
            buffer1.values - buffer2.values[:len(buffer1.values)])
    else:
        diff_values = abs(
            buffer1.values[:len(buffer2.values)] - buffer2.values)
    ax3.imshow(diff_values, aspect='auto')
    print("Accuracy: %0.4f" % (1-np.sum(diff_values != 0)/diff_values.size))
    ax3.set_title("Comparison")
    ax3.set_xlabel("Link")
    ax3.set_xticklabels(buffer1.links)
    time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    plt.savefig(time + "_deep_comparison.png", dpi=500)


def main():
    if len(sys.argv) == 2:
        plotBuffer(Buffer(sys.argv[1]))
    if len(sys.argv) == 3:
        buffers = [Buffer(sys.argv[1]), Buffer(sys.argv[2])]
        compareBufferMasks(*buffers)
        deepInspect(*buffers)


if __name__ == '__main__':
    main()
