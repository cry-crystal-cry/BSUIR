#include <iostream>
#include <ctime>


struct Stack {
	int inf = 0;
	Stack* next = nullptr;
}*st,*new_st;

Stack* create() {
	Stack* f = new Stack;
	return f;
}
Stack* create(int a) {
	Stack* f = new Stack;
	f->inf = a;
	return f;
}

Stack* add(Stack* s, int a) {
	if(s)
	{
		Stack* f = new Stack;
		f->inf = a;
		f->next = s;
		return f;
	}
	else return create(a);
}

void show(Stack* s) {
	using namespace std;
	if (!s)
		cout << "empty";
	else
	{
		while (s) {
			cout << s->inf << " ";
			s = s->next;
		}
	}
}

int found(Stack* s, int a) {
	int pos = 1;
	if (s) {
		while (s && (s->inf != a)) {
			s = s->next;
			pos++;
		}

		if (s) return pos;
		return false;

	}
	else
		return false;
}

void del(Stack** s, int a) {
	if (*s) {//if stack exist

		int pos = found(*s, a);
		Stack* f = *s;
		if (pos == 0) return;
		else
		if (pos == 1) {
			Stack* del = *s;
			(*s) = (*s)->next;
			delete del;
		}
		else if (pos == 2) {
			Stack* del = (*s)->next;
			(*s)->next = (*s)->next->next;
			delete del;
		}
		else
		{
			while (pos > 2) {//stops one el before deleted {... del, pos, ...}
				f = f->next;
				pos--;
			}

			Stack* del = f->next;
			f->next = f->next->next;
			delete del;

		}






		//if ((*s)->inf == a) {//if del first el
		//	Stack* t = *s;
		//	*s = (*s)->next;
		//	delete t;
		//}
		//else
		//{

		//	while ((*s)->next && ((*s)->next->inf != a))//searching
		//		*s = (*s)->next;

		//	if ((*s)->next) {//del
		//		Stack* t = (*s)->next;
		//		(*s)->next = (*s)->next->next;
		//		delete t;
		//	}
		//}
	}
}



void del_all(Stack** s) {
	if(*s)
	{
		while ((*s)->next)
			del(&((*s)->next), (*s)->next->inf);
		delete (*s);
		(*s) = nullptr;
	}
}

Stack* add(Stack* s) {
	return add(s, rand() % 50-25);
}

void adressSort(Stack** p) {
	if(*p)
	{
		Stack* t = NULL, * t1, * r;
		if ((*p)->next->next == NULL) return;
		do {
			for (t1 = *p; t1->next->next != t; t1 = t1->next)
				if (t1->next->inf > t1->next->next->inf) {
					r = t1->next->next;
					t1->next->next = r->next;
					r->next = t1->next;
					t1->next = r;
				}
			t = t1->next;
		} while ((*p)->next->next != t);
	}
}

void valueSort(Stack* p) {
	if(p)
	{
		Stack* t = NULL, * t1;
		int r;
		do {
			for (t1 = p; t1->next != t; t1 = t1->next)
				if (t1->inf > t1->next->inf) {
					r = t1->inf;
					t1->inf = t1->next->inf;
					t1->next->inf = r;
				}
			t = t1;
		} while (p->next != t);
	}
}

Stack* create_new_st(Stack* s) {
	if (s) {
		Stack* p, * max_p;
		int max;
		p = max_p = s;
		//p = p->next;
		max = p->inf;
		p = p->next;
		while (p) {
			if(p->inf >= max)
			{
				max = p->inf;
				max_p = p;
			}
			p = p->next;
		}

		if (s == max_p) return nullptr;
		s = s->next;//to not include head
		while (s && s != max_p) {
			new_st = add(new_st, s->inf);
			s = s->next;
		}

		return new_st;
	}
	else return nullptr;
}

void choose(Stack* st) {
	int ch = 0, d = 0;
	std::cout <<
		"\n\t1 for create stack"
		"\n\t2 for add element to stack"
		"\n\t3 for delete element for stack"
		"\n\t4 for show stack"
		"\n\t5 for sort by adress"
		"\n\t6 for sort by value"
		"\n\t7 for crete new stack with elements between head and max_el"
		"\n\tany other key to exit\n";
	std::cin >> ch;
	switch (ch) {
	case 1:
		st = create();
		choose(st);
		break;
	case 2:
		st = add(st);
		choose(st);
		break;
	case 3:
		std::cout << "type the value to delete";
		std::cin >> d;
		del(&st, d);
		choose(st);
		break;
	case 4:
		show(st);
		choose(st);
		break;
	case 5:
		adressSort(&st);
		choose(st);
		break;
	case 6:
		valueSort(st);
		choose(st);
		break;
	case 7:
		new_st = create_new_st(st);
		show(new_st);
		del_all(&new_st);
		choose(st);
		break;		
	default:
		del_all(&st);
		break;
	}
}



int main() {
	
	choose(st);

	return 0;
}