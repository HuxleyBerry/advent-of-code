#include <fstream>
#include <iostream>
#include <cstdlib>
#include <cassert>
#include <string>
#include <vector>
#include <queue>
#include <sstream>
#include <algorithm>
#include <functional>

struct Point {
    int x;
    int y;
    int z;

    std::string toString() const {
        std::ostringstream os;
        os << "(" << x << ", " << y << ", " << z << ")";
        return os.str();
    }

    void print() const {
        std::cout << x << " " << y << " " << z << "\n";
    }
};

struct PriorityQueueElement {
    long distance;
    int p;
    int q;

    PriorityQueueElement(long _distance, int _p, int _q): distance{_distance}, p{_p}, q{_q}{}
};

struct PPTreeNode {
    int parent;
    int rank; // the height of the tree down from this node
    int treeSize;
};

struct Comparer {
    bool operator()(PriorityQueueElement pair1, PriorityQueueElement pair2) {
        return pair1.distance < pair2.distance;
    }
};

long getDistanceSquared(Point p, Point q) {
    return static_cast<long>((p.x - q.x))*(p.x - q.x) + static_cast<long>((p.y - q.y))*(p.y - q.y) + static_cast<long>((p.z - q.z))*(p.z - q.z);
}

void printPriorityQueueDestructively(std::priority_queue<PriorityQueueElement, std::vector<PriorityQueueElement>, Comparer>& pq, const std::vector<Point>& points) {
    while (pq.size() > 0) {
        PriorityQueueElement el (pq.top());
        std::cout << el.distance << " " << points[el.p].toString() << " " << points[el.q].toString() << "\n";
        pq.pop();
    }
}

// returns true if we ever make a circuit of size endSize. Otherwise false.
bool merge(std::vector<PPTreeNode>& ppTree, int i, int j, int endSize) {
    int iRoot = i;
    while (ppTree[iRoot].parent != iRoot) {
        iRoot = ppTree[iRoot].parent;
    }
    int jRoot = j;
    while (ppTree[jRoot].parent != jRoot) {
        jRoot = ppTree[jRoot].parent;
    }
    if (iRoot != jRoot) {
        if (ppTree[iRoot].rank > ppTree[i].rank) {
            ppTree[jRoot].parent = iRoot;
            ppTree[iRoot].treeSize += ppTree[jRoot].treeSize;
            if (ppTree[iRoot].treeSize == endSize) {
                return true;
            }
        } else if (ppTree[i].rank < ppTree[j].rank){
            ppTree[iRoot].parent = jRoot;
            ppTree[jRoot].treeSize += ppTree[iRoot].treeSize;
            if (ppTree[jRoot].treeSize == endSize) {
                return true;
            }
        } else { // equal, so pick iRoot to be the parent of jRoot
            ppTree[jRoot].parent = iRoot;
            ppTree[iRoot].treeSize += ppTree[jRoot].treeSize;
            ++ppTree[iRoot].rank;
            if (ppTree[iRoot].treeSize == endSize) {
                return true;
            }
        }
    }
    return false;
}

int main(int argc, char** argv) {
    assert(argc >= 2);
    const int part = std::atoi(argv[1]);
    const int connectionsToMake = argc >= 3 ? std::atoi(argv[2]) : 0;

    std::ifstream is {"input.txt"};
    std::string line;
    std::vector<Point> points;
    while (std::getline(is, line)) {
        int pos = line.find(',');
        int pos2 = line.find(',', pos + 1);
        points.push_back({std::stoi(line.substr(0, pos)), std::stoi(line.substr(pos + 1, pos2 - pos)), std::stoi(line.substr(pos2 + 1))});
    }
    /*for (const auto& p: points) {
        std::cout << p.x << " " << p.y << " " << p.z << "\n";
    }*/

    std::vector<PPTreeNode> ppTree(points.size());
    for (int i = 0; i < points.size(); ++i) {
        ppTree[i] = { i, 1, 1 };
    }

    if (part == 1) {
        // we want to keep the pairs with the largest distance at the top of the priority queue
        Comparer comp;
        std::priority_queue<PriorityQueueElement,std::vector<PriorityQueueElement>, Comparer> pq;

        for (int i = 0; i < points.size(); ++i) {
            for (int j = i+1; j < points.size(); ++j) {
                long dist = getDistanceSquared(points[i], points[j]);
                if (pq.size() < connectionsToMake) {
                    pq.emplace(dist, i, j);
                } else if (pq.top().distance > dist) {
                    pq.pop();
                    pq.emplace(dist, i, j);
                }
            }
        }
        //printPriorityQueueDestructively(pq, points);

        while (pq.size() > 0) {
            PriorityQueueElement el (pq.top());
            merge(ppTree, el.p, el.q, points.size());
            pq.pop();
        }
        std::vector<int> circuitSizes;
        for (int i = 0; i < ppTree.size(); ++i) {
            if (ppTree[i].parent == i) { // i is a root
                circuitSizes.push_back(ppTree[i].treeSize);
            }
        }
        std::sort(circuitSizes.begin(), circuitSizes.end(), std::greater<int>());
        std::cout << circuitSizes[0] * circuitSizes[1] * circuitSizes[2] << "\n";

    } else if (part == 2) {
        std::vector<PriorityQueueElement> pointPairs;
        for (int i = 0; i < points.size(); ++i) {
            for (int j = i+1; j < points.size(); ++j) {
                long dist = getDistanceSquared(points[i], points[j]);
                pointPairs.emplace_back(dist, i, j);
            }
        }
        Comparer comp;
        std::sort(pointPairs.begin(), pointPairs.end(), comp);
        
        for (const auto& pair: pointPairs) {
            bool result = merge(ppTree, pair.p, pair.q, points.size());
            if (result) {
                std::cout << points[pair.p].x * points[pair.q].x << "\n";
                break;
            }
        }
    }

}