using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Data.Entity.Validation;
using System.Linq;
using System.Linq.Expressions;
using System.Text;
using System.Threading.Tasks;

namespace customer.database.data
{
    /// <summary>
    /// 作者：章建国
    /// 时间：2016-12-30
    /// </summary>
    /// <typeparam name="T"></typeparam>
    public class BaseRepository<T> where T : class
    {
        //实例化EF框架  
        private ccdmEntities db = new ccdmEntities();

        /// <summary>
        /// 新增
        /// </summary>
        /// <param name="entity">实体模型</param>
        /// <returns>操作成功返回实体，出现异常返回Null</returns>
        public T AddEntities(T entity)
        {
            try
            {
                db.Entry<T>(entity).State = EntityState.Added;
                db.SaveChanges();
            }
            catch (DbEntityValidationException dbEx)
            {
                entity = null;
            }
            return entity;
        }


        /// <summary>
        /// 修改
        /// </summary>
        /// <param name="entity">实体模型</param>
        /// <returns>操作成功返回true，操作失败或异常返回false</returns>
        public bool UpdateEntities(T entity)
        {
            try
            {
                db.Set<T>().Attach(entity);
                db.Entry<T>(entity).State = EntityState.Modified;
                return db.SaveChanges() > 0;
            }
            catch (DbEntityValidationException dbEx)
            {
                return false;
            }
        }

        /// <summary>
        /// 删除
        /// </summary>
        /// <param name="entity">实体模型</param>
        /// <returns>操作成功返回true，操作失败或异常返回false</returns>        
        public bool DeleteEntities(T entity)
        {
            try
            {
                db.Set<T>().Attach(entity);
                db.Entry<T>(entity).State = EntityState.Deleted;
                return db.SaveChanges() > 0;
            }
            catch (DbEntityValidationException dbEx)
            {
                return false;
            }
        }

        /// <summary>
        /// 返回数据集
        /// </summary>
        /// <param name="wherelambda">表达式条件</param>
        /// <returns>数据库</returns>
        public IQueryable<T> LoadEntities(System.Linq.Expressions.Expression<Func<T, bool>> wherelambda)
        {
            return db.Set<T>().Where<T>(wherelambda).AsQueryable();
        }

        /// <summary>
        /// 返回数据集
        /// </summary>
        /// <param name="wherelambda">表达式条件</param>
        /// <returns>是否成功都会返回数据集，失败数据集count为0</returns>
        public List<T> LoadListEntities(System.Linq.Expressions.Expression<Func<T, bool>> wherelambda)
        {
            try
            {
                return db.Set<T>().Where<T>(wherelambda).ToList();
            }
            catch (DbEntityValidationException dbEx)
            {
                return new List<T>();
            }
        }

        /// <summary>
        /// 返回单个实体模型
        /// </summary>
        /// <param name="entitieID">主键id</param>
        /// <returns>操作成功返回实体模型，失败返回null</returns>
        public T FindEntities(params object[] entitieID)
        {
            try
            {
                return db.Set<T>().Find(entitieID);
            }
            catch (DbEntityValidationException dbEx)
            {
                return null;
            }
        }

        /// <summary>
        /// 分页查询
        /// </summary>
        /// <typeparam name="S"></typeparam>
        /// <param name="pageSize">每页展示条数</param>
        /// <param name="pageIndex">当前页数</param>
        /// <param name="total">总条数</param>
        /// <param name="whereLambda">查询条件</param>
        /// <param name="isAsc">排序 true升序，false降序</param>
        /// <param name="orderByLambda">排序条件</param>
        /// <returns>成功或失败都将返回结果集</returns>
        public IQueryable<T> LoadPagerEntities<S>(int pageSize, int pageIndex, out int total,
            System.Linq.Expressions.Expression<Func<T, bool>> whereLambda, bool isAsc, System.Linq.Expressions.Expression<Func<T, S>> orderByLambda)
        {
            var tempData = db.Set<T>().Where<T>(whereLambda);
            total = 0;
            try
            {

                total = tempData.Count();

                //排序获取当前页的数据  
                if (isAsc)
                {
                    tempData = tempData.OrderBy<T, S>(orderByLambda).
                          Skip<T>(pageSize * (pageIndex - 1)).
                          Take<T>(pageSize).AsQueryable();
                }
                else
                {
                    tempData = tempData.OrderByDescending<T, S>(orderByLambda).
                         Skip<T>(pageSize * (pageIndex - 1)).
                         Take<T>(pageSize).AsQueryable();
                }
            }
            catch (DbEntityValidationException e)
            {

            }
            return tempData.AsQueryable();
        }

        /// <summary>
        /// 分页查询
        /// </summary>
        /// <typeparam name="S"></typeparam>
        /// <param name="pageSize">每页展示条数</param>
        /// <param name="pageIndex">当前页数</param>
        /// <param name="total">总条数</param>
        /// <param name="isAsc">排序 true升序，false降序</param>
        /// <param name="orderByLambda">排序条件</param>
        /// <returns>成功或失败都将返回结果集</returns>
        public IQueryable<T> LoadPagerEntities<S>(int pageSize, int pageIndex, out int total, bool isAsc, System.Linq.Expressions.Expression<Func<T, S>> orderByLambda)
        {
            var tempData = db.Set<T>().AsQueryable<T>();
            total = 0;
            try
            {

                total = tempData.Count();

                //排序获取当前页的数据  
                if (isAsc)
                {
                    tempData = tempData.OrderBy<T, S>(orderByLambda).
                          Skip<T>(pageSize * (pageIndex - 1)).
                          Take<T>(pageSize).AsQueryable();
                }
                else
                {
                    tempData = tempData.OrderByDescending<T, S>(orderByLambda).
                         Skip<T>(pageSize * (pageIndex - 1)).
                         Take<T>(pageSize).AsQueryable();
                }
            }
            catch (DbEntityValidationException e)
            {

            }
            return tempData.AsQueryable();
        }

        /// <summary>
        /// 用于页面持续滚动加载更多
        /// </summary>
        /// <typeparam name="S"></typeparam>
        /// <param name="offset">当前个数</param>
        /// <param name="take">获取个数</param>
        /// <param name="whereLambda">查询条件</param>
        /// <param name="isAsc">排序 true升序，false降序</param>
        /// <param name="orderByLambda">排序条件</param>
        /// <returns>成功或失败都将返回结果集</returns>
        public IQueryable<T> LoadOffSetEntities<S>(int offset, int take, System.Linq.Expressions.Expression<Func<T, bool>> whereLambda, bool isAsc, System.Linq.Expressions.Expression<Func<T, S>> orderByLambda)
        {
            var tempData = db.Set<T>().Where<T>(whereLambda);
            try
            {
                //排序获取当前页的数据  
                if (isAsc)
                {
                    tempData = tempData.OrderBy<T, S>(orderByLambda).
                          Skip<T>(offset).
                          Take<T>(take).AsQueryable();
                }
                else
                {
                    tempData = tempData.OrderByDescending<T, S>(orderByLambda).
                         Skip<T>(offset).
                         Take<T>(take).AsQueryable();
                }
            }
            catch (DbEntityValidationException e)
            {

            }
            return tempData.AsQueryable();
        }

        /// <summary>
        /// 用于页面持续滚动加载更多
        /// </summary>
        /// <typeparam name="S"></typeparam>
        /// <param name="offset">当前个数</param>
        /// <param name="take">获取个数</param>
        /// <param name="whereLambda">查询条件</param>
        /// <param name="total">总个数</param>
        /// <param name="isAsc">排序 true升序，false降序</param>
        /// <param name="orderByLambda">排序条件</param>
        /// <returns>成功或失败都将返回结果集</returns>
        public IQueryable<T> LoadOffSetEntities<S>(int offset, int take, out int total, System.Linq.Expressions.Expression<Func<T, bool>> whereLambda, bool isAsc, System.Linq.Expressions.Expression<Func<T, S>> orderByLambda)
        {
            var tempData = db.Set<T>().Where<T>(whereLambda);
            total = 0;
            try
            {
                total = tempData.Count();
                //排序获取当前页的数据  
                if (isAsc)
                {
                    tempData = tempData.OrderBy<T, S>(orderByLambda).
                          Skip<T>(offset).
                          Take<T>(take).AsQueryable();
                }
                else
                {
                    tempData = tempData.OrderByDescending<T, S>(orderByLambda).
                         Skip<T>(offset).
                         Take<T>(take).AsQueryable();
                }
            }
            catch (DbEntityValidationException e)
            {

            }
            return tempData.AsQueryable();
        }

        /// <summary>
        /// 用于页面持续滚动加载更多
        /// </summary>
        /// <typeparam name="S"></typeparam>
        /// <param name="offset">当前个数</param>
        /// <param name="take">获取个数</param>
        /// <param name="total">总个数</param>
        /// <param name="isAsc">排序 true升序，false降序</param>
        /// <param name="orderByLambda">排序条件</param>
        /// <returns>成功或失败都将返回结果集</returns>
        public IQueryable<T> LoadOffSetEntities<S>(int offset, int take, out int total, bool isAsc, System.Linq.Expressions.Expression<Func<T, S>> orderByLambda)
        {
            var tempData = db.Set<T>().AsQueryable<T>();
            total = tempData.Count();
            try
            {
                //排序获取当前页的数据  
                if (isAsc)
                {
                    tempData = tempData.OrderBy<T, S>(orderByLambda).
                          Skip<T>(offset).
                          Take<T>(take).AsQueryable();
                }
                else
                {
                    tempData = tempData.OrderByDescending<T, S>(orderByLambda).
                         Skip<T>(offset).
                         Take<T>(take).AsQueryable();
                }
            }
            catch (DbEntityValidationException e)
            {

            }
            return tempData.AsQueryable();
        }

        /// <summary>
        /// 通过sql语句查询结果
        /// </summary>
        /// <param name="sql">sql查询条件</param>
        /// <returns>返回结果集</returns>
        public IQueryable<T> LoadEntitiesBySQL(string sql)
        {
            IQueryable<T> tempData = null;
            try
            {
                tempData = db.Database.SqlQuery<T>(sql).AsQueryable<T>();
            }
            catch (DbEntityValidationException e)
            {

            }
            return tempData.AsQueryable();
        }
    }

    public static class LinqHelper
    {
        public static Expression<Func<T, bool>> AndAlso<T>(
        this Expression<Func<T, bool>> expr1,
        Expression<Func<T, bool>> expr2)
        {
            var parameter = Expression.Parameter(typeof(T));

            var leftVisitor = new ReplaceExpressionVisitor(expr1.Parameters[0], parameter);
            var left = leftVisitor.Visit(expr1.Body);

            var rightVisitor = new ReplaceExpressionVisitor(expr2.Parameters[0], parameter);
            var right = rightVisitor.Visit(expr2.Body);

            return Expression.Lambda<Func<T, bool>>(
                Expression.AndAlso(left, right), parameter);
        }

        private class ReplaceExpressionVisitor
        : ExpressionVisitor
        {
            private readonly Expression _oldValue;
            private readonly Expression _newValue;

            public ReplaceExpressionVisitor(Expression oldValue, Expression newValue)
            {
                _oldValue = oldValue;
                _newValue = newValue;
            }

            public override Expression Visit(Expression node)
            {
                if (node == _oldValue)
                    return _newValue;
                return base.Visit(node);
            }
        }
    }
}
