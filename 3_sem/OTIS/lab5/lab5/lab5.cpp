#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <stack>
#include <queue>

using namespace std;

struct Edge {
    int start, end;
    bool oriented;
    string color;
};

struct Node {
    string name;
    string shape;
    string color;
    vector<Edge> edges;
};

struct Graph {
    string name;
    vector<Node> nodes;
};

vector<Graph> graphs;

void createGraph() {
    Graph graph;
    cout << "Enter graph name: ";
    cin >> graph.name;
    graphs.push_back(graph);
}

void deleteGraph() {
    int index;
    cout << "Enter graph index: ";
    cin >> index;
    graphs.erase(graphs.begin() + index);
}

void createNode() {
    int graphIndex;
    Node node;
    cout << "Enter graph index: ";
    cin >> graphIndex;
    cout << "Enter node name: ";
    cin >> node.name;
    cout << "Enter node shape: ";
    cin >> node.shape;
    cout << "Enter node color: ";
    cin >> node.color;
    graphs[graphIndex].nodes.push_back(node);
}

void deleteNode() {
    int graphIndex, nodeIndex;
    cout << "Enter graph index: ";
    cin >> graphIndex;
    cout << "Enter node index: ";
    cin >> nodeIndex;
    graphs[graphIndex].nodes.erase(graphs[graphIndex].nodes.begin() + nodeIndex);
}

void createEdge() {
    int graphIndex, startNodeIndex, endNodeIndex;
    Edge edge;
    cout << "Enter graph index: ";
    cin >> graphIndex;
    cout << "Enter start node index: ";
    cin >> startNodeIndex;
    cout << "Enter end node index: ";
    cin >> endNodeIndex;
    cout << "Is the edge oriented? (1 for yes, 0 for no): ";
    cin >> edge.oriented;
    cout << "Enter edge color: ";
    cin >> edge.color;
    edge.start = startNodeIndex;
    edge.end = endNodeIndex;
    graphs[graphIndex].nodes[startNodeIndex].edges.push_back(edge);
}

void deleteEdge() {
    int graphIndex, startNodeIndex, endNodeIndex;
    cout << "Enter graph index: ";
    cin >> graphIndex;
    cout << "Enter start node index: ";
    cin >> startNodeIndex;
    cout << "Enter end node index: ";
    cin >> endNodeIndex;
    for (int i = 0; i < graphs[graphIndex].nodes[startNodeIndex].edges.size(); i++) {
        if (graphs[graphIndex].nodes[startNodeIndex].edges[i].end == endNodeIndex) {
            graphs[graphIndex].nodes[startNodeIndex].edges.erase(graphs[graphIndex].nodes[startNodeIndex].edges.begin() + i);
            break;
        }
    }
}

void saveGraphToFile() {
    int graphIndex;
    cout << "Enter graph index: ";
    cin >> graphIndex;
    Graph graph = graphs[graphIndex];
    string filename;
    cout << "Enter file name: ";
    cin >> filename;
    std::ofstream file(filename);
    if (file.is_open()) {
        int nodeCount = graph.nodes.size();
        file << graph.name << " " << nodeCount << std::endl;
        for (int i = 0; i < nodeCount; i++) {
            file << graph.nodes[i].name << " " << graph.nodes[i].shape << " " << graph.nodes[i].color << " " << graph.nodes[i].edges.size() << std::endl;
            for (int j = 0; j < graph.nodes[i].edges.size(); j++) {
                file << graph.nodes[i].edges[j].start << " " << graph.nodes[i].edges[j].end << " " << graph.nodes[i].edges[j].oriented << " " << graph.nodes[i].edges[j].color << std::endl;
            }
        }
        file.close();
    }
}

void readGraphFromFile() {
    Graph graph;
    string filename;
    int nodeCount;
    cout << "Enter file name: ";
    cin >> filename;
    ifstream file(filename);
    if (file.is_open()) {
        Graph graph;
        file >> graph.name >> nodeCount;
        for (int i = 0; i < nodeCount; i++) {
            Node node;
            int edgeCount;
            file >> node.name >> node.shape >> node.color >> edgeCount;
            for (int j = 0; j < edgeCount; j++) {
                Edge edge;
                file >> edge.start >> edge.end >> edge.oriented >> edge.color;
                //if (file.eof() || node.name != "") {
                //    break;
                //}
                node.edges.push_back(edge);
            }
            graph.nodes.push_back(node);
            //if (node.name == "") {
            //    graphs.push_back(graph);
            //    graph = Graph();
            //    file >> graph.name;
            //}
        }
        graphs.push_back(graph);
        file.close();
    }
}

void printDegree() {
    int graphIndex;
    cout << "Enter graph index: ";
    cin >> graphIndex;
    Graph graph = graphs[graphIndex];
    int nodeCount = graph.nodes.size();
    vector<int> degrees(nodeCount, 0);
    for (int i = 0; i < nodeCount; i++) {
        degrees[i] += graph.nodes[i].edges.size();
        for (int j = 0; j < graph.nodes[i].edges.size(); j++) {
            degrees[graph.nodes[i].edges[j].end]++;
        }
    }
    for (int i = 0; i < nodeCount; i++) {
        cout << "Node " << i << " has degree " << degrees[i] << endl;
    }
}

void printDegree(int& graphIndex) {
    Graph graph = graphs[graphIndex];
    int nodeCount = graph.nodes.size();
    vector<int> degrees(nodeCount, 0);
    for (int i = 0; i < nodeCount; i++) {
        degrees[i] += graph.nodes[i].edges.size();
        for (int j = 0; j < graph.nodes[i].edges.size(); j++) {
            degrees[graph.nodes[i].edges[j].end]++;
        }
    }
    for (int i = 0; i < nodeCount; i++) {
        int degree = graph.nodes[i].edges.size();
        cout << "Node " << i << " has degree " << degrees[i] << endl;
    }
}
void printIncidenceMatrix() {
    int graphIndex;
    cout << "Enter graph index: ";
    cin >> graphIndex;
    Graph graph = graphs[graphIndex];
    int nodeCount = graph.nodes.size();
    int edgeCount = 0;
    for (int i = 0; i < nodeCount; i++) {
        edgeCount += graph.nodes[i].edges.size();
    }
    int** incidenceMatrix = new int* [nodeCount];
    for (int i = 0; i < nodeCount; i++) {
        incidenceMatrix[i] = new int[edgeCount];
        for (int j = 0; j < edgeCount; j++) {
            incidenceMatrix[i][j] = 0;
        }
    }
    int edgeIndex = 0;
    for (int i = 0; i < nodeCount; i++) {
        for (int j = 0; j < graph.nodes[i].edges.size(); j++) {
            Edge edge = graph.nodes[i].edges[j];
            incidenceMatrix[i][edgeIndex] = 1;
            incidenceMatrix[edge.end][edgeIndex] = 1;
            edgeIndex++;
        }
    }
    for (int i = 0; i < nodeCount; i++) {
        for (int j = 0; j < edgeCount; j++) {
            cout << incidenceMatrix[i][j] << " ";
        }
        cout << endl;
    }
    for (int i = 0; i < nodeCount; i++) {
        delete[] incidenceMatrix[i];
    }
    delete[] incidenceMatrix;
}

void printIncidenceMatrix(int& graphIndex) {
    Graph graph = graphs[graphIndex];
    int nodeCount = graph.nodes.size();
    int edgeCount = 0;
    for (int i = 0; i < nodeCount; i++) {
        edgeCount += graph.nodes[i].edges.size();
    }
    int** incidenceMatrix = new int* [nodeCount];
    for (int i = 0; i < nodeCount; i++) {
        incidenceMatrix[i] = new int[edgeCount];
        for (int j = 0; j < edgeCount; j++) {
            incidenceMatrix[i][j] = 0;
        }
    }
    int edgeIndex = 0;
    for (int i = 0; i < nodeCount; i++) {
        for (int j = 0; j < graph.nodes[i].edges.size(); j++) {
            Edge edge = graph.nodes[i].edges[j];
            incidenceMatrix[i][edgeIndex] = 1;
            incidenceMatrix[edge.end][edgeIndex] = 1;
            edgeIndex++;
        }
    }
    for (int i = 0; i < nodeCount; i++) {
        for (int j = 0; j < edgeCount; j++) {
            cout << incidenceMatrix[i][j] << " ";
        }
        cout << endl;
    }
    for (int i = 0; i < nodeCount; i++) {
        delete[] incidenceMatrix[i];
    }
    delete[] incidenceMatrix;
}

bool isComplete() {
    int graphIndex;
    cout << "Enter graph index: ";
    cin >> graphIndex;
    Graph graph = graphs[graphIndex];
    int nodeCount = graph.nodes.size();
    int edgeCount = 0;
    for (int i = 0; i < nodeCount; i++) {
        edgeCount += graph.nodes[i].edges.size();
    }
    return edgeCount == nodeCount * (nodeCount - 1) / 2;
}

bool isComplete(int& graphIndex) {
    Graph graph = graphs[graphIndex];
    int nodeCount = graph.nodes.size();
    int edgeCount = 0;
    for (int i = 0; i < nodeCount; i++) {
        edgeCount += graph.nodes[i].edges.size();
    }
    return edgeCount == nodeCount * (nodeCount - 1) / 2;
}

void printAdjaencyList() {
    int graphIndex;
    cout << "Enter graph index: ";
    cin >> graphIndex;
    int nodeCount = graphs[graphIndex].nodes.size();

    vector<vector<int>> adjaencyList(nodeCount);
    for (int i = 0; i < nodeCount; i++) {
        for (int j = 0; j < graphs[graphIndex].nodes[i].edges.size(); j++) {
            int nodeFrom = i;
            int nodeTo = graphs[graphIndex].nodes[i].edges[j].end;
            adjaencyList[nodeFrom].push_back(nodeTo);
            adjaencyList[nodeTo].push_back(nodeFrom);
        }
    }

    for (int i = 0; i < nodeCount; i++) {   //вывод списка инцидентности для проверки
        cout << i << ": ";
        for (int j = 0; j < adjaencyList[i].size(); j++)
            cout << adjaencyList[i][j] << " ";
        cout << endl;
    }
}

void makeComplete() {
    int graphIndex;
    cout << "Enter graph index: ";
    cin >> graphIndex;
    int nodeCount = graphs[graphIndex].nodes.size();

    vector<vector<int>> adjaencyList(nodeCount);
    for (int i = 0; i < nodeCount; i++) {
        for (int j = 0; j < graphs[graphIndex].nodes[i].edges.size(); j++) {
            int nodeFrom = i;
            int nodeTo = graphs[graphIndex].nodes[i].edges[j].end;
            adjaencyList[nodeFrom].push_back(nodeTo);
            adjaencyList[nodeTo].push_back(nodeFrom);
        }
    }

    /*for (int i = 0; i < nodeCount; i++) {   //вывод списка инцидентности для проверки
        cout << i << ": ";
        for (int j = 0; j < adjaencyList[i].size(); j++)
            cout << adjaencyList[i][j] << " ";
        cout << endl;
    }*/


    vector<vector<int>> needToAddEdge(nodeCount);
    for (int i = 0; i < nodeCount - 1; i++) {       //вершина для которой выбриается список инцидентности
        for (int j = i + 1; j < nodeCount; j++) {   //вершина которую мы проверяем есть ли она в списке
            bool edgeExist = false;
            for (int k = 0; k < adjaencyList[i].size(); k++) {   //бегунок всех элементов в списке инцедентности выбраной вершины
                if (j == adjaencyList[i][k]) {
                    edgeExist = true;
                    break;
                }
            }
            if (edgeExist == false) {
                Edge edge;
                edge.start = i;
                edge.end = j;
                edge.color = "not selected because makeComplete() used";
                edge.oriented = 0;
                graphs[graphIndex].nodes[i].edges.push_back(edge);
            }
        }
    }

    /*adjaencyList.clear();      //вывод списка инцидентности для проверки
    adjaencyList.resize(nodeCount);
    for (int i = 0; i < nodeCount; i++) {
        for (int j = 0; j < graphs[graphIndex].nodes[i].edges.size(); j++) {
            int nodeFrom = i;
            int nodeTo = graphs[graphIndex].nodes[i].edges[j].end;
            adjaencyList[nodeFrom].push_back(nodeTo);
            adjaencyList[nodeTo].push_back(nodeFrom);
        }
    }
    for (int i = 0; i < nodeCount; i++) {
        cout << i << ": ";
        for (int j = 0; j < adjaencyList[i].size(); j++)
            cout << adjaencyList[i][j] << " ";
        cout << endl;
    }*/
}

void printGraphInfo() {
    int graphIndex;
    cout << "Enter graph index: ";
    cin >> graphIndex;
    Graph graph = graphs[graphIndex];
    int nodeCount = graph.nodes.size();
    int edgeCount = 0;
    for (int i = 0; i < nodeCount; i++) {
        edgeCount += graph.nodes[i].edges.size();
    }
    cout << "Graph name: " << graph.name << endl;
    cout << "Number of nodes: " << nodeCount << endl;
    cout << "Number of edges: " << edgeCount << endl;
    cout << "Graph complete if 1, not comlete if 0: " << isComplete(graphIndex) << endl;
    printDegree(graphIndex);
    printIncidenceMatrix(graphIndex);
}

void dfs(int v, vector<vector<int>>& adj, vector<bool>& used, vector<int>& res) {
    used[v] = true;
    for (int u : adj[v]) {
        if (!used[u]) {
            dfs(u, adj, used, res);
        }
    }
    res.push_back(v);
}

void eulerCycle() {
    int graphIndex;
    cout << "Enter graph index: ";
    cin >> graphIndex;
    Graph graph = graphs[graphIndex];
    int nodeCount = graph.nodes.size();
    vector<vector<int>> adj(nodeCount);
    for (int i = 0; i < nodeCount; i++) {
        for (int j = 0; j < graphs[graphIndex].nodes[i].edges.size(); j++) {
            int nodeFrom = i;
            int nodeTo = graphs[graphIndex].nodes[i].edges[j].end;
            adj[nodeFrom].push_back(nodeTo);
            adj[nodeTo].push_back(nodeFrom);
        }
    }

    int n = adj.size();
    vector<int> in(n), out(n);
    for (int i = 0; i < n; i++) {
        for (int j : adj[i]) {
            in[j]++;
            out[i]++;
        }
    }
    int start = 0;
    while (start < n && in[start] == out[start]) {
        start++;
    }
    if (start == n) {
        start = 0;
    }
    vector<bool> used(n);
    vector<int> res;
    dfs(start, adj, used, res);
    reverse(res.begin(), res.end());

    for (int i = 0; i < res.size(); i++) {
        cout << res[i] << " ";
    }
}

void printAllPathsUtil(int u, int d, bool visited[], int path[], int& path_index, vector<vector<int>>& adj)
{
    visited[u] = true;
    path[path_index] = u;
    path_index++;

    if (u == d) {
        for (int i = 0; i < path_index; i++)
            cout << path[i] << " ";
        cout << endl;
    }
    else {
        for (auto i = adj[u].begin(); i != adj[u].end(); ++i)
            if (!visited[*i])
                printAllPathsUtil(*i, d, visited, path, path_index, adj);
    }

    path_index--;
    visited[u] = false;
}

void printShortestPath(int& s, int& d, vector<vector<int>>& adj)
{
    queue<int> q;
    vector<int> dist(adj.size(), INT_MAX);
    vector<int> parent(adj.size(), -1);

    q.push(s);
    dist[s] = 0;

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        for (auto i = adj[u].begin(); i != adj[u].end(); ++i) {
            if (dist[*i] == INT_MAX) {
                dist[*i] = dist[u] + 1;
                parent[*i] = u;
                q.push(*i);
            }

            if (*i == d) {
                cout << "Shortest path length is : " << dist[*i] << endl;
                cout << "Path is:: ";
                int curr = d;
                while (curr != -1) {
                    cout << curr << " ";
                    curr = parent[curr];
                }
                cout << endl;
                return;
            }
        }
    }
}
vector<vector<int>> convertGraphToAdjacencyList(int& graphIndex) {
    int nodeCount = graphs[graphIndex].nodes.size();

    vector<vector<int>> adjaencyList(nodeCount);
    for (int i = 0; i < nodeCount; i++) {
        for (int j = 0; j < graphs[graphIndex].nodes[i].edges.size(); j++) {
            int nodeFrom = i;
            int nodeTo = graphs[graphIndex].nodes[i].edges[j].end;
            adjaencyList[nodeFrom].push_back(nodeTo);
            adjaencyList[nodeTo].push_back(nodeFrom);
        }
    }
    return adjaencyList;
}

void printAllPaths()
{
    int graphIndex, s, d;
    cout << "Enter graph index: ";
    cin >> graphIndex;
    cout << "Enter index of node to start: ";
    cin >> s;
    cout << "Enter index of node to destinantion: ";
    cin >> d;
    vector<vector<int>>adj = convertGraphToAdjacencyList(graphIndex);
    bool* visited = new bool[adj.size()];
    for (int i = 0; i < adj.size(); i++)
        visited[i] = false;

    int* path = new int[adj.size()];
    int path_index = 0;

    printAllPathsUtil(s, d, visited, path, path_index, adj);
    cout << "\n\n";
    printShortestPath(s, d, adj);
}



int main() {
    int choice;
    do {
        cout << "Graph Editor" << endl;
        cout << "1. Create graph" << endl;
        cout << "2. Delete graph" << endl;
        cout << "3. Create node" << endl;
        cout << "4. Delete node" << endl;
        cout << "5. Create edge" << endl;
        cout << "6. Delete edge" << endl;
        cout << "7. Save graph" << endl;
        cout << "8. Load graph" << endl;
        cout << "9. Print graph info" << endl;
        cout << "10. Print degree" << endl;
        cout << "11. Print incidence matrix" << endl;
        cout << "12. Make graph complete" << endl;
        cout << "13. Search Euler circuit" << endl;
        cout << "14. Search all paths and shortiest one" << endl;
        cout << "15. Print adjaency list" << endl;
        cout << "0. Exit" << endl;
        cout << "Enter choice: ";
        cin >> choice;
        switch (choice) {
        case 1:
            createGraph();
            break;
        case 2:
            deleteGraph();
            break;
        case 3:
            createNode();
            break;
        case 4:
            deleteNode();
            break;
        case 5:
            createEdge();
            break;
        case 6:
            deleteEdge();
            break;
        case 7:
            saveGraphToFile();
            break;
        case 8:
            readGraphFromFile();
            break;
        case 9:
            printGraphInfo();
            break;
        case 10:
            printDegree();
            break;
        case 11:
            printIncidenceMatrix();
            break;
        case 12:
            makeComplete();
            break;
        case 13:
            eulerCycle();
            break;
        case 14:
            printAllPaths();
            break;
        case 15:
            printAdjaencyList();
            break;
        case 0:
            cout << "Goodbye!" << endl;
            break;
        default:
            cout << "Invalid choice. Try again." << endl;
            break;
        }
    } while (choice != 0);

    return 0;
}