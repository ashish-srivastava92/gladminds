package sfa.mc.bajaj.gladminds.com.bajaj_mc_sfa;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import android.content.ActivityNotFoundException;
import android.content.DialogInterface;
import android.net.Uri;

public class ListImageAdapter extends BaseAdapter
{

	Activity context;
	String get_retails_name[];
	String get_retails_contact_number[];



	public ListImageAdapter(Activity context, String[] retails_name,String[] retails_contact) {
		super();
		this.context = context;
		this.get_retails_name = retails_name;
		this.get_retails_contact_number = retails_contact;

	}

	public int getCount() {
		return get_retails_name.length;
	}

	public Object getItem(int position) {
		// TODO Auto-generated method stub
		return null;
	}

	public long getItemId(int position) {
		// TODO Auto-generated method stub
		return 0;
	}

	private class ViewHolder {
        TextView tv_field_retails_nm;
        TextView tv_field_retails_number;
		TextView tv_retail_date,job_name,job_pri,job_place;
        //ImageView img_ph_nm,img_mobile_nm,img_email;
	}

	public View getView(int position, View convertView, ViewGroup parent)
	{
		// TODO Auto-generated method stub
		ViewHolder holder;
		LayoutInflater inflater =  context.getLayoutInflater();

		if (convertView == null)
		{
//			Typeface font = Typeface.createFromAsset(context.getAssets(), "LinotypeZapfino One.ttf");
			convertView = inflater.inflate(R.layout.retail_list_item, null);
			holder = new ViewHolder();
			holder.tv_field_retails_nm = (TextView) convertView.findViewById(R.id.tv_retail_name);
			holder.tv_field_retails_number = (TextView) convertView.findViewById(R.id.tv_retail_contact);

			
			//holder.img_ph_nm = (ImageView) convertView.findViewById(R.id.imv_ph_call);
			//holder.img_mobile_nm = (ImageView) convertView.findViewById(R.id.imv_mobile_call);
			//holder.img_email = (ImageView) convertView.findViewById(R.id.imv_email);
			convertView.setTag(holder);
		}
		else
		{
			holder = (ViewHolder) convertView.getTag();
		}

		holder.tv_field_retails_nm.setText(get_retails_name[position]);
		holder.tv_field_retails_number.setText(get_retails_contact_number[position]);




	return convertView;
	}




}
