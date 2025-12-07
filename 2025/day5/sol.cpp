#include <iostream>
#include <string>
#include <fstream>
#include <cstdlib>
#include <cassert>
#include <vector>
#include <utility>
#include <algorithm>
#include <unordered_map>
#include <sstream>
#include <stdexcept>
#include <set>

enum class RangeStatus {
    SPOILED,
    FRESH,
    UNKNOWN
};

struct SegmentTreeNode {
    RangeStatus status = RangeStatus::SPOILED;
    long min;
    long max;
    bool isLeaf = false;
    bool isJunk = true;
};

typedef std::vector<SegmentTreeNode> SegmentTree;

int getLeftChildIndex(int currIndex) {
    return (currIndex+1)*2 - 1;
}

int getRightChildIndex(int currIndex) {
    return (currIndex+1)*2;
}

std::string rangeStatusToString(RangeStatus r) {
    switch (r) {
        case RangeStatus::SPOILED:
            return "Spoiled";
        case RangeStatus::FRESH:
            return "Fresh";
        case RangeStatus::UNKNOWN:
            return "Unknown";
        default:
            throw std::invalid_argument("WTF!");
    }
}

std::string segmentTreeNodeToString(const SegmentTreeNode& stn) {
    if (stn.isJunk) {
        return "Junk";
    }
    std::ostringstream is;
    is << stn.min << "-" << stn.max << ": " << rangeStatusToString(stn.status);
    return is.str();
}

void printSegmentTree(const SegmentTree& segmentTree) {
    int index = 0;
    int nodesPerLevel = 1;
    bool breakRequired = false;
    bool leafOnlyRowFound = false;
    while (!leafOnlyRowFound) {
        bool nonLeafOrJunkFound = false;
        for (int i = index; i < index+nodesPerLevel; ++i) {
            if (!segmentTree[i].isLeaf && !segmentTree[i].isJunk) {
                nonLeafOrJunkFound = true;
            }
            std::cout << segmentTreeNodeToString(segmentTree[i]) << "\t";
        }
        index += nodesPerLevel;
        nodesPerLevel *= 2;
        std::cout <<"\n\n";
        if (!nonLeafOrJunkFound) {
            leafOnlyRowFound = true;
        }
    }
}

int bisectRange(int left, int right) {
    return (right + left)/2;
}

void setUpSegmentTree(SegmentTree& segmentTree, const std::vector<std::pair<long,long>>& partitionedSpace, size_t treeIndex, int nodeLeft, int nodeRight) {
    segmentTree[treeIndex].isJunk = false;
    segmentTree[treeIndex].min = partitionedSpace[nodeLeft].first;
    segmentTree[treeIndex].max = partitionedSpace[nodeRight].second;
    if (nodeLeft != nodeRight) {
        int leftHalfEnd = bisectRange(nodeLeft, nodeRight);
        int rightHalfStart = leftHalfEnd+1;
        setUpSegmentTree(segmentTree, partitionedSpace, getLeftChildIndex(treeIndex), nodeLeft, leftHalfEnd);
        setUpSegmentTree(segmentTree, partitionedSpace, getRightChildIndex(treeIndex), rightHalfStart, nodeRight);
    } else {
        segmentTree[treeIndex].isLeaf = true;
    }
}

void setUpSegmentTree(SegmentTree& segmentTree, const std::vector<std::pair<long,long>>& partitionedSpace) {
    return setUpSegmentTree(segmentTree, partitionedSpace, 0, 0, partitionedSpace.size() - 1);
}

// The range [nodeIndex-nodeRight] is the interval represented by index treeIndex in the segment tree
void freshenRange(SegmentTree& segmentTree, size_t treeIndex, int rangeStart, int rangeEnd, int nodeLeft, int nodeRight) {
    assert(rangeStart >= nodeLeft && rangeEnd <= nodeRight);
    if (segmentTree[treeIndex].status != RangeStatus::FRESH){
        if (rangeStart == nodeLeft && rangeEnd == nodeRight) {
            segmentTree[treeIndex].status = RangeStatus::FRESH;
        } else {
            // the range does not correspond 1-1 with a node in the segment tree
            // we need to go down another level in the tree
            segmentTree[treeIndex].status = RangeStatus::UNKNOWN;
            int leftEnd = bisectRange(nodeLeft, nodeRight);
            int rightStart = leftEnd+1;
            if (rangeStart <= leftEnd) {
                freshenRange(segmentTree, getLeftChildIndex(treeIndex), rangeStart, std::min(leftEnd, rangeEnd), nodeLeft, leftEnd);
            }
            if (rangeEnd >= rightStart) {
                freshenRange(segmentTree, getRightChildIndex(treeIndex), std::max(rightStart, rangeStart), rangeEnd, rightStart, nodeRight);
            }
        }
    }
}

void freshenRange(SegmentTree& segmentTree, int rangeStart, int rangeEnd, int endPointsCount) {
    assert(rangeStart >= 0 && rangeEnd < endPointsCount);
    freshenRange(segmentTree, 0, rangeStart, rangeEnd, 0, endPointsCount-1);
}

bool querySegmentTree(const SegmentTree& segmentTree, long query, size_t treeIndex) {
    if (query < segmentTree[treeIndex].min || query > segmentTree[treeIndex].max) {
        return false;
    } else if (segmentTree[treeIndex].status == RangeStatus::FRESH) {
        return true;
    } else if (segmentTree[treeIndex].status == RangeStatus::SPOILED) {
        return false;
    } else {
        assert(!segmentTree[treeIndex].isLeaf); // a leaf node should not have status unknown
        return querySegmentTree(segmentTree, query, getLeftChildIndex(treeIndex)) || querySegmentTree(segmentTree, query, getRightChildIndex(treeIndex));
    }
}

bool querySegmentTree(const SegmentTree& segmentTree, long query) {
    return querySegmentTree(segmentTree, query, 0);
}

long countFresh(const SegmentTree& segmentTree, size_t treeIndex) {
    if (segmentTree[treeIndex].status == RangeStatus::FRESH) {
        return segmentTree[treeIndex].max - segmentTree[treeIndex].min + 1;
    } else if (segmentTree[treeIndex].status == RangeStatus::SPOILED) {
        return 0;
    } else {
        assert(!segmentTree[treeIndex].isLeaf); // a leaf node should not have status unknown
        return countFresh(segmentTree, getLeftChildIndex(treeIndex)) + countFresh(segmentTree, getRightChildIndex(treeIndex));
    }
}

long countFresh(const SegmentTree& segmentTree) {
    return countFresh(segmentTree, 0);
}

int main(int argc, char** argv) {
    assert(argc >= 2);
    int part = std::atoi(argv[1]);

    std::ifstream is {"input.txt"};
    std::string line;
    std::vector<std::pair<long,long>> ranges;
    std::vector<long> queries;
    std::set<long> rangeEndpoints;
    bool rangesDone = false;
    std::unordered_map<long, int> rangeEndpointsToIndex;
    while(std::getline(is, line)) {
        if (line.size() == 0) {
            rangesDone = true;
            continue;
        } else if (rangesDone) {
            queries.push_back(std::atol(line.c_str()));
        } else {
            size_t pos = line.find('-');
            assert(pos != std::string::npos);
            long left = std::atol(line.substr(0,pos).c_str());
            long right = std::atol(line.substr(pos+1).c_str());
            assert(left <= right);
            rangeEndpoints.insert(left);
            rangeEndpoints.insert(right);
            ranges.push_back(std::pair(left, right));
        }
    }

    std::vector<long> rangeEndpointsVector;
    for (long n: rangeEndpoints) {
        rangeEndpointsVector.push_back(n);
    }
    
    int partitionedSpaceElementCount = 0;
    std::vector<std::pair<long,long>> partitionedSpace;
    for (size_t i = 0; i < rangeEndpointsVector.size() - 1; ++i) {
        partitionedSpace.emplace_back(rangeEndpointsVector[i],rangeEndpointsVector[i]);
        rangeEndpointsToIndex[rangeEndpointsVector[i]] = partitionedSpaceElementCount;
        ++partitionedSpaceElementCount;
        if (rangeEndpointsVector[i+1] - rangeEndpointsVector[i] > 1) {
            partitionedSpace.emplace_back(rangeEndpointsVector[i]+1,rangeEndpointsVector[i+1]-1);
            ++partitionedSpaceElementCount;
        }
    }
    partitionedSpace.emplace_back(rangeEndpointsVector[rangeEndpointsVector.size() - 1],rangeEndpointsVector[rangeEndpointsVector.size() - 1]);
    rangeEndpointsToIndex[rangeEndpointsVector[rangeEndpointsVector.size() - 1]] = partitionedSpaceElementCount;
    ++partitionedSpaceElementCount;

    SegmentTree segmentTree(4*partitionedSpace.size(), {RangeStatus::SPOILED, 0, 0, false, true});
    setUpSegmentTree(segmentTree, partitionedSpace);
    //printSegmentTree(segmentTree);
    
    for (const auto& pair: ranges) {
        freshenRange(segmentTree, rangeEndpointsToIndex[pair.first], rangeEndpointsToIndex[pair.second], partitionedSpaceElementCount);
    }
    if (part == 1) {
        std::cout << std::count_if(queries.cbegin(), queries.cend(), [&segmentTree](long q){
            return querySegmentTree(segmentTree, q);
        }) << "\n";
    } else if (part == 2) {
        std::cout << countFresh(segmentTree) << "\n";
    }
}