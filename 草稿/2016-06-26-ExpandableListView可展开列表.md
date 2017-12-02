​	[ExpandableListView](https://developer.android.com/reference/android/widget/ExpandableListView.html)

​	[ExpandableListActivity](https://developer.android.com/reference/android/app/ExpandableListActivity.html)

​	ExpandableListView ，可展开的 ListView，是 ListView 的子类，可以将 item 显示在垂直滚动的双层列表中。它与 ListView 的区别就在于可以双层显示：分组显示 children。而这些 item将从该 view 关联的 ExpandableListAdapter 中得到。

​	可展开列表允许在每一个 item 旁边显示一个指示器，用于指示 item 的当前状态（展开的 group、折叠的 group、child 或 last child）。



## ExpandableListActivity

​	ExpandableListActivity 是 Activity 的一个子类，用于显示一个可展开的列表，并提供了一些用于选择 item 的事件处理，如：onChildClick(…)、onGroupCollapse(…)、onGroupExpand(...)等。



### screen 布局

​	ExpandableListActivity 提供了一个默认的布局，如果需要自定义，需要在布局中添加 id 为 @android:list 的 ExpandableListView。

​	也可以选择性地设置一个在列表为空时显示的视图，该视图的 id 必须为 @id/android:empty。



### Row 布局

​	ExpandableListActivity 使用 setListAdapter(ExpandableListAdapter) 方法来设置 ExpandableListAdapter，以为每一行提供视图。该 adapter 使用单独的方法来提供 group 视图和 child 视图。Android 提供了几个可用的 ExpandableListAdapter： SimpleCursorTreeAdapter 和 SimpleExpandableListAdapter，其中， SimpleCursorTreeAdapter 从 Cursor 中获取数据，而 SimpleExpandableListAdapter 从 List 或 Map 中获取数据。



### 数据绑定

​	通过 ExpandableListAdapter 接口的实现类来将数据绑定到 ExpandableListView。Android 提供了两个标准的 adapter： SimpleExpandableListAdapter、SimpleCursorTreeAdapter 。



## ExpandableListAdapter

​	ExpandableListAdapter 与一般 ListView 的 Adapter 不一样，它是一个单独的 interface。系统提供了两个实现ExpandableListAdapter的抽象类：SimpleExpandableListAdapter、SimpleCursorTreeAdapter。

```java
public interface ExpandableListAdapter {
    void registerDataSetObserver(DataSetObserver observer);
    void unregisterDataSetObserver(DataSetObserver observer);
    int getGroupCount();
    int getChildrenCount(int groupPosition);
    Object getGroup(int groupPosition);
    Object getChild(int groupPosition, int childPosition);
    long getGroupId(int groupPosition);
    long getChildId(int groupPosition, int childPosition);
    boolean hasStableIds();
    View getGroupView(int groupPosition, boolean isExpanded, View convertView, ViewGroup parent);
    View getChildView(int groupPosition, int childPosition, boolean isLastChild,
            View convertView, ViewGroup parent);
    boolean isChildSelectable(int groupPosition, int childPosition);
    boolean areAllItemsEnabled();
    boolean isEmpty();
    void onGroupExpanded(int groupPosition);
    void onGroupCollapsed(int groupPosition);
    long getCombinedChildId(long groupId, long childId);
    long getCombinedGroupId(long groupId);
}

```

### SimpleExpandableListAdapter



### SimpleCursorTreeAdapter

​	将 cursor 中的 column 映射到定义在 XML 中的TextView 或 ImageView，并且可以为 child 和 group 分别指定 XML 文件。

​	绑定分为两个阶段：

​	首先，如果 SimpleCursorTreeAdapter.ViewBinder 可用，将调用setViewValue(android.view.View, android.database.Cursor, int)。返回值为 true 说明发生了绑定。如果返回 false 并且将要绑定的 view 是一个 TextView，将会调用 setViewText(TextView, String)；如果返回 false 且将要绑定的 view 是 ImageView，则会调用setViewImage(ImageView, String)。

​	SimpleCursorTreeAdapter 是一个抽象类，它的抽象方法只有一个：

```java
//为给定的 group 提供包含 children 的 cursor，如果需要异步进行查询，则可以直接返回 null，然后
//通过 setChildrenCursor(int, Cursor) 来设置
abstract protected Cursor getChildrenCursor(Cursor groupCursor);
```

​	构造函数：

```java
	//从参数名称就可以基本知道其意义，其中 cursor 与 group 对应     
	public SimpleCursorTreeAdapter(Context context, Cursor cursor, int collapsedGroupLayout,
            int expandedGroupLayout, String[] groupFrom, int[] groupTo, int childLayout,
            int lastChildLayout, String[] childFrom, int[] childTo) {
        ...
    }
    public SimpleCursorTreeAdapter(Context context, Cursor cursor, int collapsedGroupLayout,
            int expandedGroupLayout, String[] groupFrom, int[] groupTo,
            int childLayout, String[] childFrom, int[] childTo) {
        ...
    }
    public SimpleCursorTreeAdapter(Context context, Cursor cursor, int groupLayout,
            String[] groupFrom, int[] groupTo, int childLayout, String[] childFrom,
            int[] childTo) {
        ...
    }
```