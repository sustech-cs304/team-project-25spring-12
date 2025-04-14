import { defineStore } from 'pinia';

interface ListItem {
	name: string;
	path: string;
	title: string;
}

export const useTabsStore = defineStore('tabs', {
	state: () => ({
		list: <ListItem[]>[]
	}),
	getters: {
		show: state => state.list.length > 0,
		nameList: state => state.list.map(item => item.name)
	},
	actions: {
		delTabsItem(index: number) {
			this.list.splice(index, 1);
		},
		setTabsItem(data: ListItem) {
			if (!this.list.find(item => item.path === data.path)) {
				this.list.push(data);
			}
		},
		clearTabs() {
			this.list = [];
		},
		closeTabsOther(data: ListItem[]) {
			this.list = data;
		},
		closeCurrentTag(router: any, currentPath: string) {
			const index = this.list.findIndex(item => item.path === currentPath);
			if (index !== -1) {
				const isLast = index === this.list.length - 1;
				const next = isLast ? this.list[index - 1] : this.list[index + 1];
				this.list.splice(index, 1);
				router.push(next?.path || '/');
			}
		}
	}
});