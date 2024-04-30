$(document).ready(function(){
	$('.top__main_language-text').click(function(){
		$('.top__main_language-select').toggle();
	});
	$('.top__main_language-ru').click(function(){
		$('.top__main_language-text span').text('Ru');
		$('.all').addClass('ru');
		$('.all').removeClass('en');
		$('.top__main_language-select').hide();
	});
	$('.top__main_language-en').click(function(){
		$('.top__main_language-text span').text('En');
		$('.all').removeClass('ru');
		$('.all').addClass('en');
		$('.top__main_language-select').hide();
	});
	$('.jq-selectbox__select1').click(function(){
		$('.jq-selectbox__dropdown1').toggle();
	});
	$('.jq-selectbox__dropdown1 li').click(function(){
		$('.jq-selectbox__dropdown1').hide();
		$('.jq-selectbox__select-text1').text($(this).text());
	});
	$('.jq-selectbox__select2').click(function(){
		$('.jq-selectbox__dropdown2').toggle();
	});
	$('.jq-selectbox__dropdown2 li').click(function(){
		$('.jq-selectbox__dropdown2').hide();
		$('.jq-selectbox__select-text2').text($(this).text());
	});
	$('.jq-selectbox__select3').click(function(){
		$('.jq-selectbox__dropdown3').toggle();
	});
	$('.jq-selectbox__dropdown3 li').click(function(){
		$('.jq-selectbox__dropdown3').hide();
		$('.jq-selectbox__select-text3').text($(this).text());
	});
	$('.jq-selectbox__select4').click(function(){
		$('.jq-selectbox__dropdown4').toggle();
	});
	$('.jq-selectbox__dropdown4 li').click(function(){
		$('.jq-selectbox__dropdown4').hide();
		$('.jq-selectbox__select-text4').text($(this).text());
	});
	$('.jq-selectbox__select5').click(function(){
		$('.jq-selectbox__dropdown5').toggle();
	});
	$('.jq-selectbox__dropdown5 li').click(function(){
		$('.jq-selectbox__dropdown5').hide();
		$('.jq-selectbox__select-text5').text($(this).text());
	});
});