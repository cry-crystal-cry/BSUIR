#include <iostream>
#include <ctime>

class list {
public:
	int inf = 0;
	list* next = nullptr, * prev = nullptr;
}*begin, *end,*new_begin,*new_end;

void create(list** begin,list** end) {
	list* f = new list;
	(*begin) = (*end) = f;
}
void create(int a, list** begin, list** end) {
	create(begin, end);
	(*begin)->inf = a;
}

void add_end(list** begin,list** end, int a) {
	if (*end)
	{
		list* f = new list;
		f->inf = a;
		(*end)->prev = f;
		f->next = (*end);
		*end = f;
	}else 
		create(a, begin, end);
	
}

void add_begin(list** begin, list** end, int a) {
	if (*begin)
	{
		list* f = new list;
		f->inf = a;
		f->prev = (*begin);
		(*begin)->next = f;
		*begin = f;
	}else 
		create(a, begin, end);

}

void show_begin(list* s) {
	using namespace std;
	if (!s) 
		cout << "empty\n";
	else
	{
		while (s != nullptr) {
			cout << s->inf << " ";
			s = s->prev;
		}
	}
}

void show_end(list* s) {
	using namespace std;
	if (!s)
		cout << "empty\n";
	else
	{
		while (s != nullptr) {
			cout << s->inf << " ";
			s = s->next;
		}
	}
}

int found(list* s, int a) {//searching by *end;
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

void del(list** s, int a) {//del by *end;
	if (*s) {//if stack exist

		int pos = found(*s, a);
		list* f = *s;
		if (pos == 0) return;
		else
		if (pos == 1) {
			list* del = *s;
			
			if((*s)->next)
				(*s)->next->prev = nullptr;
			(*s) = (*s)->next;
			delete del;
		}
		else if (pos == 2) {
			list* del = (*s)->next;
			(*s)->next = (*s)->next->next;
			(*s)->next->next->prev = (*s);
			delete del;
		}
		else
		{
			while (pos > 2) {//stops one el before deleted {... del, f, ...}
				f = f->next;
				pos--;
			}
			if (f->next->next) {//if el is not first like {... x, del, f, ...}
				list* del = f->next;
				f->next = f->next->next;
				f->next->next->prev = f;
				delete del;
			}
			else { //if el is first like {del, f, ...}
				list* del = f->next;
				f->next = f->next->next;
				delete del;
			}

		}
	}
}



void del_all(list** s) {//del by *end;
	if(*s)
	{
		while ((*s)->next)
			del(&((*s)->next), (*s)->next->inf);
		delete (*s);
		(*s) = nullptr;
	}
}
void create_new_l(list* begin, list** new_begin, list** new_end) {
	if (begin) {
		list* p, * max_p;
		int max;
		p = max_p = begin;
		max = p->inf;
		p = p->prev;
		while (p) {
			if (p->inf >= max)
			{
				max = p->inf;
				max_p = p;
			}
			p = p->prev;
		}

		if (begin == max_p) return ;
		begin = begin->prev;//to not include head
		while (begin && begin != max_p) {
			add_end(new_begin, new_end, begin->inf);
			begin = begin->prev;
		}
	}
}
void choose(list* begin, list* end) {
	int ch = 0, d = 0;
	std::cout <<
		"\n\t1 for create list"
		"\n\t2 for add element to begin of list"
		"\n\t3 for add element to end of list"
		"\n\t4 for delete element for list"
		"\n\t5 for show stack from begin"
		"\n\t6 for show stack from end"
		"\n\t7 for crete new stack with elements between head and max_el"
		"\n\tany other key to exit\n";
	std::cin >> ch;
	switch (ch) {
	case 1:
		del_all(&end);
		create(&begin, &end);
		choose(begin, end);
		break;
	case 2:
		add_begin(&begin, &end, rand() % 50 - 25);
		choose(begin, end);
		break;
	case 3:
		add_end(&begin, &end, rand() % 50 - 25);
		choose(begin, end);
		break;
	case 4:
		std::cout << "type the value to delete";
		std::cin >> d;
		del(&end, d);
		choose(begin, end);
		break;
	case 5:
		show_begin(begin);
		choose(begin, end);
		break;
	case 6:
		show_end(end);
		choose(begin, end);
		break;
	case 7:
		create_new_l(begin,&new_begin,&new_end);

		show_begin(new_begin);
		del_all(&new_end);
		choose(begin, end);
		break;
	default:
		del_all(&end);
		break;
	}
}

int main() {
	choose(begin, end);


}