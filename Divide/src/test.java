
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.StringReader;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.wltea.analyzer.lucene.IKAnalyzer;
 

public class test {
	public static void main(String[] args) throws Exception {
		BufferedReader br = new BufferedReader(new FileReader("training.txt"));//构造一个BufferedReader类来读取文件
		FileWriter fw = new FileWriter("training_result.txt");  
		String text = "随着互联网移动支付的迅速普及，我们享受到越来越多的生活便利。如当您走入商场的某家餐厅时，手机会自动弹出该餐厅的优惠券；当您走入商场服装店时，手机可以自动推荐这家店里您喜欢的衣服；在您路过商场一家珠宝店时，手机可以自动提示您想了很久的一款钻戒已经有货了；离开商场停车场时，手机在您的许可下可以自动交停车费。这些您所享受的贴心服务都离不开背后大数据挖掘和机器学习的支持。在正确的时间、正确的地点给用户最有效的服务，是各大互联网公司智能化拓展的新战场。本赛题目标为在商场内精确的定位用户当前所在商铺。在真实生活中，当用户在商场环境中打开手机的时候，存在定位信号不准、环境信息不全、店铺信息缺失、不同店铺空间距离太近等等挑战，因此如何精确的判断用户所在商铺是一个难题。本次大赛我们将提供在2017年8月份大概100家商场的详细数据，包括用户定位行为和商场内店铺等数据（已脱敏），参赛队伍需要对其进行数据挖掘和必要的机器学习训练。另外，我们会提供2017年9月份的商场内用户数据来做评测，检测您的算法是否能准确的识别出当时用户所在的店铺。";
		Analyzer analyzer = new IKAnalyzer(true);
		StringReader reader = null;
		while((text = br.readLine())!=null){//使用readLine方法，一次读一行
			text = text.trim();
			/*for(int i=0; i<text.length();i++)
			{
				if(text.charAt(i) == 'X' || text.charAt(i) == 'x' )
					text
			}*/
			text = text.replaceAll("(x|X)", " ");
			//text = text.substring(1);
			text = text.trim();
			reader = new StringReader(text);
			TokenStream ts = analyzer.tokenStream("", reader);  
	        CharTermAttribute term=(CharTermAttribute) ts.getAttribute(CharTermAttribute.class); 
	        while(ts.incrementToken()){  
	        	String s = term.toString()+"|";
	            System.out.print(s);  
	            fw.write(s,0,s.length()); 
	            
	        }
	        fw.write("\r\n",0,1); 
	        fw.flush(); 
	        System.out.println();
        }
		fw.close();
        br.close();
		
        analyzer.close();
        reader.close();  
	}
}
