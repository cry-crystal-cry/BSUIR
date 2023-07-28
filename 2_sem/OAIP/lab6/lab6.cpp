#include <iostream>

struct tree {
	int key;
	char str[10]={"12asd"};
	tree* left = nullptr, * right = nullptr;
}*bereza;

int len_str(tree* t) {
	int len = 0;
	while (t->str[len] != '\0')len++;
	return len;
}

void create(tree*& t, int a) {
	t = new tree;
	t->key = a;
}

void create(tree*&t) {
	int value;
	std::cout << "enter first element";
	std::cin >> value;
	create(t, value);
}

void add(tree*& t) {
	int value;
	std::cout << "enter value to add";
	std::cin >> value;
	tree* s = t, *prev = t;
	if (t) {
		while (s)
			if (value > s->key)
			{
				prev = s;
				s = s->right;
			}
			else if (value < s->key)
			{
				prev = s;
				s = s->left;
			}
			else return;
		tree* new_el = new tree;
		new_el->key = value;
		if (value < prev->key)
			prev->left = new_el;
		else prev->right = new_el;

	}
	else
		 create(t,value);
}

void show(tree* t, int level) {
	if (t) {
		show(t->right, level + 1);
		for (int i = 0; i < level; i++)
			std::cout << "  ";
		std::cout << t->key<<"\n";
		show(t->left, level + 1);
	}
}

void show(tree* t) {
	show(t, 0);
}

void del(tree** t,int value) {
	if(*t)
	{
		tree* to_del, * prev_del = nullptr, * replace, * prev_replace;
		to_del = *t;
		while (to_del && to_del->key != value) {
			prev_del = to_del;
			if (to_del->key < value)
				to_del = to_del->right;
			else
				to_del = to_del->left;
		}
		if (!to_del) return;

		prev_replace = to_del;
		if (to_del->left == nullptr)
			replace = to_del->right;
		else
			if (to_del->right == nullptr)
				replace = to_del->left;
			else {
				replace = to_del->left;
				while (replace->right) {
					prev_replace = replace;
					replace = replace->right;
				}

				if (prev_replace == to_del)
					replace->right = to_del->right;
				else {
					replace->right = to_del->right;
					prev_replace->right = replace->left;
					replace->left = to_del->left;///////////////////
				}
			}
		if (to_del == *t) *t = replace;
		else
			if (to_del->key < prev_del->key)
				prev_del->left = replace;
			else
				prev_del->right = replace;
		delete to_del;
	}
}

void del_all(tree** t) {
	if (*t) {
		del_all(&(*t)->left);
		del_all(&(*t)->right);
		delete (*t);
	}
}

int fun(tree* t) {
	int count = 0;
	if(!t->left&&!t->right)
		return len_str(t);
	if (t->left)
		count += fun(t->left);
	if (t->right)
		count += fun(t->right);
	count += len_str(t);
	return count;
}

void choose(tree* t) {
	int ch = 0, d = 0;
	std::cout <<
		"\n\t1 for create tree"
		"\n\t2 for add element to tree"
		"\n\t3 for delete element from tree"
		"\n\t4 for show tree"
		"\n\t5 for count number of charecters in all strings of tree"
		"\n\tany other key to exit\n";
	std::cin >> ch;
	switch (ch) {
	case 1:
		del_all(&t);
		create(t);
		choose(t);
		break;
	case 2:
		add(t);
		choose(t);
		break;
	case 3:
		std::cout << "type the value to delete";
		std::cin >> d;
		del(&t, d);
		choose(t);
		break;
	case 4:
		show(t);
		choose(t);
		break;
	case 5:
		std::cout<<fun(t);
		choose(t);
		break;
	default:
		del_all(&t);
		break;
	}
}

int main() {
	
	choose(bereza);

}